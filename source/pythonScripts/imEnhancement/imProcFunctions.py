# File of processing images and performing image enhancement
# importing the required module
import math
import matplotlib.colors as colors
import numpy as np
import scipy.signal as sps


def normalize(image, reqmean=None, reqvar=None):
    """
    Author: Riley Campbell

    Normalizes the image in 'image' parameter to a mean specified by the 'mean'
    parameter, and a standard deviation specified by the 'std' paramter.

    :param image: Input image to be normalized
    :param reqmean: The mean to normailze the image to
    :param reqvar: The standard deviation to normalize the image to.

    :return: The normalized image
    """

    arg1 = reqmean is None
    arg2 = reqvar is None
    # Verify the correct number of arguments are 1 or 3
    if (arg1 and not arg2) or (arg2 and not arg1):
        print('No of arguments must be 1 or 3')
        return image

    # If only one argument is passed in, just normalise 0 - 1
    if arg1 and arg2:
        # Assume color image
        if np.ndim(image) == 3:
            hsv = colors.rgb_to_hsv(image)
            v = hsv[:, :, 2]
            v = v - np.min(v)  # Just normalise value component
            v = v / np.max(v)
            hsv[:, :, 2] = v
            normim = colors.hsv_to_rgb(hsv)

        else:  # Assume greyscale
            numpyImage = np.array(image, dtype=float)
            npmin = np.min(numpyImage)
            normim = numpyImage - npmin
            npmax = np.max(normim)
            normim = normim / npmax

    else:  # 3 arguments passed in normalise to desired mean and variance
        # determine if color image
        if np.ndim(image) == 3:
            print('cannot normalise color image to desired mean and variance')
            return image

        numpyImage = np.array(image, dtype=float)

        # Convert image to have zero mean and unit std dev
        npMean = np.mean(numpyImage)
        numpyImage = numpyImage - npMean

        npStd = np.std(numpyImage)
        numpyImage = numpyImage / npStd

        # Now convert image to have the required mean and variance
        normim = reqmean + numpyImage * math.sqrt(reqvar)

    return normim


def medFilt2D(image):
    """
Author: Riley Campbell

Applies a median filter to the image held in the function parameter 'image'.

:param image: Input image to be normalized

:return: The median filtered image.
"""

    # Apply a median filter to the image
    medFiltIm = sps.medfilt2d(np.array(image, float))

    return medFiltIm


def stdBlocKProc2d(image, blkHeight, blkWidth):
    """
Author: Riley Campbell

stdBlocKProc2D processes the image 'image' for calculating the standard deviation.
This function should divide the image into blocks with a height specified
by 'blkHeight' and a width specified by 'blkWidth'. Then for each block in
the image, the standard deviation of the pixel values in that block is
determined and stored in a mask. For each block, this is equivalent to
lining up all the pixel values in the block and finding the standard
deviation between them. The mask returned should have the same dimensions
as the original image, and it should be divided into blocks just like the
original image. For each block in the mask, every pixel value in that block
should be the calculated standard deviation from that same block found in
the original image. This function should return this mask.


:param image: Input image to block process for the standard deviation
:param blkHeight: The height of each block to divide the image into
:param blkWidth: The width of each block to divide the image into

:return: A mask containing the block processed standard deviations.
"""
    # error checking
    height = image.shape[0]
    width = image.shape[1]

    # if less than 1, set to 1
    blkWidth = max(1, blkWidth)
    blkHeight = max(1, blkHeight)

    # if greater than image, set to image max
    blkWidth = min(width, blkWidth)
    blkHeight = min(height, blkHeight)
    stdMask = np.array(image, dtype=float)

    # compute the std matrix
    for i in range(0, height, blkHeight):
        for j in range(0, width, blkWidth):
            iEnd = min(height, i + blkHeight)
            jEnd = min(width, j + blkWidth)
            block = stdMask[i:iEnd, j:jEnd]
            stdMask[i:iEnd, j:jEnd] = np.std(block)

    return stdMask
