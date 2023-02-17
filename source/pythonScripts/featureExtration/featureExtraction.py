import numpy as np
import io, os,sys,inspect
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from scipy.spatial import ConvexHull
from skimage.filters import threshold_otsu
from skimage.morphology import skeletonize
import subprocess
from PIL import Image, ImageOps
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
from minutiaeSet import minutiae


class ImageFeature:
    """
    Helper class to track image information.
    """
    def __init__(self, locX, locY, orientation, fType=None):
        """
        Initialize the class.
        Args:
            locX: feature x coordinate
            locY: feature y coordinate
            orientation: feature orientation in degrees
            fType: feature type, default None
        """
        self.__locX = locX
        self.__locY = locY
        self.__orientation = orientation
        self.__fType = fType

    def degrees(self):
        """
        Get the orientation of the feature in degrees.
        Returns: orientation
        """
        return self.__orientation

    def fType(self):
        """
        Get the type of feature (i.e. bifurcation, ridge ending, etc)
        Returns: feature type
        """
        return self.__fType

    def loc(self):
        """
        Get the x, y coordinates of the feature.
        Returns: feature x, y location

        """
        return self.__locX, self.__locY

    def radians(self):
        """
        Get the orientation of the feature in radians.
        Returns: orientation
        """
        return math.radians(self.__orientation)


class MinutiaeSet:
    """Sets of known minutiae patterns.
    """
    def __init__(self):
        self.__minutiaeSet = []
        self.loadDefaultSet()

    def getMinutiaeSet(self):
        return self.__minutiaeSet

    def loadDefaultSet(self):
        # minutiae 1
        self.__minutiaeSet = minutiae 


class Node:
    """Node class for BFS.
    """
    def __init__(self, loc):
        self.adjacent = []
        self.loc = loc
        self.visited = False


def binaryImageToGraph(A):
    adj_list = {}
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            adj_list[(j, i)] = []

            if A[i, j] == 1:
                if i > 0 and j > 0:
                    if A[i - 1, j - 1] == 1:
                        adj_list[(j, i)].append((j - 1, i - 1))
                if i > 0:
                    if A[i - 1, j] == 1:
                        adj_list[(j, i)].append((j, i - 1))
                    if j + 1 < A.shape[1]:
                        if A[i - 1, j + 1] == 1:
                            adj_list[(j, i)].append((j + 1, i - 1))
                if j > 0:
                    if A[i, j - 1] == 1:
                        adj_list[(j, i)].append((j - 1, i))
                    if i + 1 < A.shape[0]:
                        if A[i + 1, j - 1] == 1:
                            adj_list[(j, i)].append((j - 1, i + 1))

                if i + 1 < A.shape[0] and j + 1 < A.shape[1]:
                    if A[i + 1, j + 1] == 1:
                        adj_list[(j, i)].append((j + 1, i + 1))
                if i + 1 < A.shape[0]:
                    if A[i + 1, j] == 1:
                        adj_list[(j, i)].append((j, i + 1))
                if j + 1 < A.shape[1]:
                    if A[i, j + 1] == 1:
                        adj_list[(j, i)].append((j + 1, i))

    node_list = []
    for key, value in adj_list.items():
        # if a node has no neighbors, don't add it into the adjacency list
        if len(value) > 0:
            node = Node(key)
            node.adjacent = value
            node_list.append(node)

    return node_list


def convertImage(img):
    """Invert image, convert to binary, and skeleton-ize.

    Args:
        img : numpy array containing image data

    Returns:
        sk_img : numpy array containing converted image data
    """

    # complement
    #c_img = np.invert(img)

    # make binary
    #c_img = imgToBinary(c_img)

    # skeleton-ize
    sk_img = skeletonize(img)

    return sk_img


def euclideanDistance(A, B):
    """Find the Euclidean distance between two 2D points.
    Args:
        A: point A
        B: point B

    Returns:
        Euclidean distance between A and B
    """
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**(1/2.0)


def findFeatures(skele_img, org_img, seg_mask):
    """
    Given a skeleton-ized image, use Harris Corner Detection to find features.
    Args:
        img: skeleton-ized image

    Returns: list of features, [ImageFeature]

    """
    height, width = org_img.shape
    features = []

    # Create minutiae set
    minutiae_set = MinutiaeSet().getMinutiaeSet()
    pad = 10    # skip the first n rows and columns
    mask_pad = 15
    for row in range(pad, skele_img.shape[0] - pad - 1):
        for col in range(pad, skele_img.shape[1] - pad - 1):
            # 3x3 window around point
            window = skele_img[row-1:row+2, col-1:col+2]
            if col - mask_pad > 0 and seg_mask[row,col-mask_pad] \
            and col + mask_pad < width and seg_mask[row, col+mask_pad] \
            and row - mask_pad > 0 and seg_mask[row-mask_pad,col] \
            and row + mask_pad < height and seg_mask[row+mask_pad,col]:
                if isMinutiae(window, minutiae_set):
                    orientation = findMinutiaeOrientation(row, col, skele_img)
                    features.append(ImageFeature(col, row, orientation))

    return features


def findMinutiaeOrientation(i, j, thinIm):
    """Find the orientation in degrees of a feature centered at i, j.
    Args:
        i: row
        j: col
        thinIm: image

    Returns:
        orientation in degrees
    """
    # return orientation in degrees
    # Process ridge endings
    crossing_number = 0
    coords = []
    for p in range(i-1, i+2):
        for q in range(j-1, j+2):
            if (p != i or q != j) and thinIm[p, q] > 0:
                coords.append((p, q))
                crossing_number += 1

    # use a nxn window with i, j at the center
    # NOTE: this code uses [x (col), y (row)] style coordinates, which are
    #       the reverse of the coordinates used by numpy.shape
    window_size = (31, 31)
    window_origin = [window_size[0] // 2, window_size[1] // 2]

    # TODO: how to indicate an error? this isn't great because 0 is a valid angle
    # check that the window doesn't overstep the bounds of the array
    if i + window_origin[1] >= thinIm.shape[0] or i - window_origin[1] < 0:
        return 0
    if j + window_origin[0] >= thinIm.shape[1] or j - window_origin[0] < 0:
        return 0

    # ridge ending
    if crossing_number == 1:
        distances = findRidgeOrientation(thinIm, i, j, window_size, window_origin, bifurcation=False)

        # angle between distances[0] and center point
        coord = distances[0][0]     # the (row, col) tuple for the furthest point
        x = coord[0] - window_origin[0]
        y = coord[1] - window_origin[1]
        degrees = 180 + math.atan2(y, x) * 180 / math.pi
        return (degrees + 360) % 360

    # bifurcation
    if crossing_number == 3:
        distances = findRidgeOrientation(thinIm, i, j, window_size, window_origin, bifurcation=True)

        # angle between distances[0], distances[1],
        # and distances[2] (three furthest points) and the center point
        dirs = []
        for d in distances[:3]:
            coord = d[0]
            x = coord[0] - window_origin[0]
            y = coord[1] - window_origin[1]
            degrees = math.atan2(y, x) * 180 / math.pi
            dirs.append((degrees + 360) % 360)

        # Find which ridge direction differs the most from the rest
        dirs.sort()

        if dirs[1] - dirs[0] > dirs[2] - dirs[1]:
            return dirs[0]
        else:
            return dirs[2]

    # TODO: how to indicate an error? this isn't great because 0 is a valid angle
    return 0


def findRidgeOrientation(thinIm, center_i, center_j, window_size, window_origin, bifurcation):
    """Use breadth first search to trace ridges away from the feature origin
       up to some given distance (within a 5x5 matrix for example). Once the
       path through the graph is found, find distance between each point on the
       path and the origin. Sort the list of point-distance pairs in descending
       order and return this list.
    Args:
        thinIm: skeleton-ized image
        center_i: row of feature center
        center_j: col of feature center
        window_size: the size of the graph
        window_origin: tuple of coordinates at center of graph
        bifurcation: True if minutiae is bifurcation, False otherwise. Determines
                     whether a convex hull can be formed around the vertices.

    Returns:
        list of angles between each point and the origin
    """
    i_start = center_i - (window_size[1] // 2)
    i_end = center_i + (window_size[1] // 2)
    j_start = center_j - (window_size[0] // 2)
    j_end = center_j + (window_size[0] // 2)

    # using a 5x5 grid centered on center_i, center_j
    # convert the binary image into a graph
    node_list = binaryImageToGraph(1 * thinIm[i_start:i_end+1, j_start:j_end+1])

    start = 0
    for idx, node in enumerate(node_list):
        if list(node.loc) == window_origin:
            start = idx

    # Given a list of Node objects, perform BFS
    # Create path
    path = []

    # Create a queue for BFS, mark the source node as
    # visited and enqueue it
    queue = [node_list[start]]
    node_list[start].visited = True

    while queue:
        # Dequeue a vertex from
        # queue and print it
        s = queue.pop(0)
        path.append(list(s.loc))

        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        for i in s.adjacent:
            for node in node_list:
                if node.loc == i:
                    if node.visited is False:
                        node.visited = True
                        queue.append(node)

    vertices = []
    if bifurcation:
        # if there are more than 3 points in the path, find the convex hull
        # of all the points in the BFS
        hull = ConvexHull(path, 'QbB')
        vertices = [path[h] for h in hull.vertices]
    else:
        vertices = path

    # for each point on the convex hull, find its distance from origin
    distances = []
    for vertex in vertices:
        distances.append([vertex, euclideanDistance(vertex, window_origin)])

    # return reverse sorted list of hull vertex distances from origin
    distances.sort(reverse=True, key=lambda node: node[1])
    return distances


def imgToBinary(img):
    """Convert image to binary using thresholding.
       https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_thresholding.html

    Args:
        img : numpy array with image data

    Returns:
        img : numpy array with binary image data

    >>> imgToBinary(np.array([[129, 128], [128, 129]]))
    array([[1, 0],
           [0, 1]])
    """

    thresh = threshold_otsu(img)
    return 1 * (img > thresh)


def isMinutiae(window, minutiae_set):
    """Given a window into a larger image, determine if the center point is
       an image feature.

    Args:
        window: sub-matrix of larger image
        minutiae_set: set of known minutiae

    Returns:
        True: center point of window is minutiae
        False: center point of window is not minutiae
    """
    if window.shape != (3, 3):
        print("window must be a 3x3 numpy matrix")
        print(window.shape)
        return False

    # Middle pixel in window must be value of 1 for it to be considered minutia
    if window[1, 1] == False:
        return False

    theWindow = np.zeros(window.shape)
    for i in range(len(theWindow)):
        for j in range(len(theWindow)):
            if window[i,j] == True:
                theWindow[i,j] = 1
 
    # Identify candidate minutiae using the crossing number technique 
    count = -1
    for i in range(len(window)):
        for j in range(len(window[0])):
            if window[i,j] == True:
                count = count + 1    

    # TODO Remove Debugging statement for identifying missing minutiae
    if count == 1 or count == 3:
        # Match window to set of known minutia
        for m in minutiae_set:
            # TODO: does this do what you think it does?
            if (m == theWindow).all():
                return True
        print(theWindow)
        print()
        return False

    return False


def plotFeatures(img, features, title="Image Features"):
    """Plot features over an image.

    Args:
        img : numpy array containing image data
        features : list of image features, [ImageFeature]
    """
    fig, ax = plt.subplots(1)
    ax.imshow(img, cmap='gray')

    # add the feature to the plot
    for f in features:
        showFeature(f.loc()[0], f.loc()[1], f.degrees(), ax, scale=1.2)

    plt.title(title)
    plt.axis(False)
    plt.show()


def showFeature(x, y, orientation, ax, scale=1):
    """This function will display a red square centered on x, y with a line
       drawn from the center point of the square to the edge of the square
       indicating the dominant orientation.

    Args:
        x : x coordinate of the feature
        y : y coordinate of the feature
        orientation : orientation of the feature in degrees
        ax : the axis on which to plot the feature
        scale : the scale of the feature. Defaults to 1.
    """
    # set the width & height based on scale
    width = 10 * scale
    height = 10 * scale

    # overlay the rectangle on the axis
    ts = ax.transData
    tr = transforms.Affine2D().rotate_deg_around(x, y, orientation)
    rect = patches.Rectangle((x - int(width / 2), y - int(height / 2)), width,
                             height, linewidth=1, edgecolor='r',
                             facecolor='none', transform=(tr + ts))
    ax.add_patch(rect)

    # overlay the line to indicate orientation
    p1 = [x, y]
    p2 = [x + int(width / 2), y]

    x_vals = [p1[0], p2[0]]
    y_vals = [p1[1], p2[1]]

    ax.plot(x_vals, y_vals, linewidth=1, color='r', transform=(tr + ts))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
