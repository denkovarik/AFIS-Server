# File of processing images and performing image enhancement
import numpy as np
import matplotlib
#import matplotlib.pyplot as plt
import matplotlib.image as mping
from scipy import signal
from scipy import ndimage, misc
import math
import matplotlib.colors as colors
import scipy.signal as sps
from PIL import Image, ImageOps
from scipy.ndimage import uniform_filter


def derivative7(im, dim):
    """
    Author: Dennis Kovarik

    This function computes 1st and 2nd derivatives of an image using the 7-tap
    coefficients given by Farid and Simoncelli.

    :param image: Input image to compute derivatives from
    :param dim: character that can be 'x' or 'y' for what to compute the
                dirivatives in respect to.
    :return: The first dirivative in x or y
    """
    p = np.array([0.004711, 0.069321, 0.245410, 0.361117, 0.245410, 0.069321, 0.004711])
    d1 = np.array([0.018708, 0.125376, 0.193091, 0.000000, -0.193091, -0.125376, -0.018708])

    dirIm = np.copy(im)

    # Check what to find the 1st dirivative in respect to
    if dim == 'x':
        # Convolve columns of image
        for j in range(np.size(im, 1)):
            dirIm[:, j] = np.convolve(p[:], dirIm[:, j], mode='same')
        for i in range(np.size(im, 0)):
            dirIm[i, :] = np.convolve(d1[:], dirIm[i, :], mode='same')
    # Check what to find the 1st dirivative in respect to
    elif dim == 'y':
        # Convolve columns of image
        for j in range(np.size(im, 1)):
            dirIm[:, j] = np.convolve(d1[:], dirIm[:, j], mode='same')
        for i in range(np.size(im, 0)):
            dirIm[i, :] = np.convolve(p[:], dirIm[i, :], mode='same')

    else:
        print("Second argument must be either 'x' or 'y'. ")
        print("No opertaion was performed.")

    return dirIm


def enhanceFingerprintImage(im):
    """
    This function performs fingerprint image enhancement on a fingerprint
    image. This function will segment and enhance the image to produce an
    unthinned and a thinned binary enhanced fingerprint image. This function
    will return the enhanced fingerprint image as a PIL image, the unthinned
    binary fingerprint as a 2D numpy array, and the segmentation mask as a 2D
    numpy array.

    :param im: The fingerprint image to enhance as a PIL image
    :return: The enhanced fingerprint image as a PIL image
    :return: The unthinned binary fingerprint as a 2D numpy array
    :return: The fingerprint segmentatin mask as a 2D numpy array
    """
    # Get the height and width of the image
    orgiImWidth, orgiImHeight = im.size
    aspectRatio = orgiImWidth / orgiImHeight

    # Resize the Image
    newImHeight = 500
    newImWidth = int(newImHeight * aspectRatio)
    resizedIm = im.resize((newImWidth, newImHeight))

    # Convert to grayscale
    grayIm = ImageOps.grayscale(resizedIm)

    # Convert to 2D numpy array
    arrIm = np.array(grayIm)

    # Normalize the image
    normim = normalize(arrIm, 0, 1)

    # Construct a segmentation mask for the fingerprint image
    segMask2DArr = ridgeSegment(normim)

    # Ensure Fingerprint Image is Light on Dark
    if isDarkRidgesOnWhite(arrIm, segMask2DArr):
        grayIm = ImageOps.invert(grayIm)
        # Convert to 2D numpy array
        arrIm = np.array(grayIm)
        # Normalize the image
        normim = normalize(arrIm, 0, 1)
    
    # Determine ridge orientations
    orientim, dummy, dummy = ridgeorient(normim, 1, 5, 5)

    blksze = 36
    dummy, medfreq = ridgefreq(normim, segMask2DArr, orientim, blksze, 5, 5, 15)

    # Actually I find the median frequency value used across the whole
    # fingerprint gives a more satisfactory result...
    freq = medfreq * segMask2DArr

    # Now apply filters to enhance the ridge pattern
    grayEnhancedIm = ridgefilter(normim, orientim, freq, 0.5, 0.5, 1)

    grayEnhancedIm[grayEnhancedIm > 0] = 255

    # Binarise, ridge/valley threshold is 0
    binEnhancedIm = grayEnhancedIm >= 1

    # Convert Binary Unthinned Fingerprint 2D Numpy Array to PIL image
    enhancedImg = Image.fromarray(np.invert(binEnhancedIm))

    return enhancedImg, binEnhancedIm, segMask2DArr



def freqest(im, orientim, windsze, minWaveLength, maxWaveLength):
    """
    FREQEST - Estimate fingerprint ridge frequency within image block

    Function to estimate the fingerprint ridge frequency within a small block
    of a fingerprint image.  This function is used by RIDGEFREQ

    Usage:
      freqim =  freqest(im, orientim, windsze, minWaveLength, maxWaveLength)

    Arguments:
             im       - Image block to be processed. A 2D numpy array
             orientim - Ridge orientation image of image block. A 2D numpy
                        array, should be same size as im
             windsze  - Window length used to identify peaks. This should be
                        an odd integer, say 3 or 5.
             minWaveLength,  maxWaveLength - Minimum and maximum ridge
                         wavelengths, in pixels, considered acceptable.
                         should be ints

     Returns:
             freqim    - An image block the same size as im with all values
                         set to the estimated ridge spatial frequency.  If a
                         ridge frequency cannot be found, or cannot be found
                         within the limits set by min and max Wavlength
                         freqim is set to zeros. should be a 2D numpy array of
                         same size as im

     Suggested parameters for a 500dpi fingerprint image
       freqim = freqest(im,orientim, 5, 5, 15)

    See also:  RIDGEFREQ, RIDGEORIENT, RIDGESEGMENT


    Peter Kovesi
    School of Computer Science & Software Engineering
    The University of Western Australia
    pk at csse uwa edu au
    http://www.csse.uwa.edu.au/~pk

    January 2005
    """

    # convert image to numpy array
    im = np.array(im)
    orientim = np.array(orientim)

    rows = im.shape[0]
    cols = im.shape[1]

    # Find mean orientation within the block. This is done by averaging the
    # sines and cosines of the doubled angles before reconstructing the
    # angle again.  This avoids wraparound problems at the origin.
    orientim = 2 * orientim
    cosorient = np.mean(np.cos(orientim))
    sinorient = np.mean(np.sin(orientim))
    orient = np.arctan2(sinorient, cosorient) / 2

    # Rotate the image block so that the ridges are vertical
    # rotim = ndimage.rotate(im, orient / math.pi * 180 + 90, mode='nearest')
    rotim = imRotate(im, orient / math.pi * 180 + 90)

    # Now crop the image so that the rotated image does not contain any
    # invalid regions.  This prevents the projection down the columns
    # from being mucked up.
    cropsze = math.floor(rows / math.sqrt(2))
    offset = math.floor((rows - cropsze) / 2) - 1
    rotim = rotim[offset:offset + cropsze + 1, offset: offset + cropsze + 1]

    # Sum down the columns to get a projection of the grey values down
    # the ridges.
    proj = np.array([rotim.sum(axis=0)])

    # Find peaks in projected grey values by performing a greyscale
    # dilation and then finding where the dilation equals the original
    # values.
    # dilation = ndimage.rank_filter(proj, rank=(windsze - 1), size=(1, windsze))
    dilation = ordfilt2(proj, windsze, np.ones(shape=((1, windsze))))
    maxpts = np.array((abs(dilation - proj) < 0.0001) & (proj > np.nanmean(proj)) * 1)
    maxind = np.flatnonzero(maxpts)

    # Determine the spatial frequency of the ridges by dividing the
    # distance between the 1st and last peaks by the (No of peaks-1). If no
    # peaks are detected, or the wavelength is outside the allowed bounds,
    # the frequency image is set to 0
    if len(maxind) < 2:
        freqim = np.zeros(np.shape(im))
    else:
        NoOfPeaks = len(maxind)
        maxind = np.array(maxind)
        waveLength = (maxind[-1] - maxind[0]) / (NoOfPeaks - 1)
        if waveLength > minWaveLength and waveLength < maxWaveLength:
            freqim = 1 / waveLength * np.ones(np.shape(im))
        else:
            freqim = np.zeros(np.shape(im))

    return freqim


def gauss2DKernal(shape=(3, 3), sigma=0.5):
    """
    This function constructs and returns a 2D gaussian mask for gaussian
    filtering.

    :param shape: The dimensions of the kernal.
    :param sigma: The standard deviation for the kernal
    :return: A 2D kernal for gaussian filtering
    """
    m, n = [(ss - 1.) / 2. for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    h = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def gaussFilt(im, h, w, sigma):
    """
    This function will apply gaussian filtering to the h x w matrix 'im' passed
    into the function.

    :param im: A 'h' by 'w' image, represented as a 2D numpy array, for
               applying gaussian filtering to.
    :param h: The height of the kernal
    :param w: The width of the kernal
    :param sigma: The standard deviation for the kernal
    :return: The image 'im' with gaussian filtering applied to it.
    """
    kernal = gauss2DKernal(shape=(h, w), sigma=sigma)
    return signal.convolve2d(im, kernal, mode='same')


def imRotate(im, angle, method=None):
    """
    This function will rotate and crop 'im' by the specified angle using a
    specified method. This function will default to using the Nearest
    method for rotating the image, but it will use the Bilinear method if
    specified by the function parameter 'method'.

    :param im: The image, as a 2D numpy array to rotate and crop
    :param angle: The angle to rotate the image by in degrees
    :param method: The method used for rotating the image
    :return: The rotated image as a 2D numpy array
    """
    npIm = Image.fromarray(im)  # Convert to PIL image
    # Rotate
    if not method is None and method == "bilinear":
        npIm = npIm.rotate(angle, resample=Image.BILINEAR)
    else:
        npIm = npIm.rotate(angle, resample=Image.NEAREST)

    rotim = np.array(npIm)  # Convert back to numpy array
    return rotim


def isDarkRidgesOnWhite(imArr, segMask):
    """
    Determines if the image, passed into the function as a 2D numpy array, is
    such that the ridges of the fingerprint are dark while the background is
    light in color.

    :param imArr: The fingerprint image passed in as a 2D numpy array
    :param segMask: Mask identifying the fingerprint from the background
    :return: Boolen of whether the fingerprint image is black on white
    """
    forgroundAvg = np.average(imArr[segMask == True])
    backgroundAvg = np.average(imArr[segMask == False])
    if forgroundAvg < backgroundAvg:
        return True
    return False


def ordfilt2(proj, windsze, domain):
    """
    Performs 2D order statics filtering on elements in a 2D numpy array.

    :param proj: 2D numpy array to filter
    :param windsze: Element to replace target pixel
    :param domain: Numeric array specifing the domain for filtering operations
    :return: The filtered array as a 2D numpy array.
    """
    return ndimage.rank_filter(proj, rank=(windsze - 1), footprint=domain, mode="constant", cval=0)


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


'''
# RIDGEFILTER - enhances fingerprint image via oriented filters
#
# Function to enhance fingerprint image via oriented filters
#
# Usage:
#  newim =  ridgefilter(im, orientim, freqim, kx, ky, showfilter)
#
# Arguments:
#         im       - Image to be processed.
#         orientim - Ridge orientation image, obtained from RIDGEORIENT.
#         freqim   - Ridge frequency image, obtained from RIDGEFREQ.
#         kx, ky   - Scale factors specifying the filter sigma relative
#                    to the wavelength of the filter.  This is done so
#                    that the shapes of the filters are invariant to the
#                    scale.  kx controls the sigma in the x direction
#                    which is along the filter, and hence controls the
#                    bandwidth of the filter.  ky controls the sigma
#                    across the filter and hence controls the
#                    orientational selectivity of the filter. A value of
#                    0.5 for both kx and ky is a good starting point.
#         showfilter - An optional flag 0/1.  When set an image of the
#                      largest scale filter is displayed for inspection.
#
# Returns:
#         newim    - The enhanced image
#
# See also: RIDGEORIENT, RIDGEFREQ, RIDGESEGMENT

# Reference:
# Hong, L., Wan, Y., and Jain, A. K. Fingerprint image enhancement:
# Algorithm and performance evaluation. IEEE Transactions on Pattern
# Analysis and Machine Intelligence 20, 8 (1998), 777 789.

# Peter Kovesi
# School of Computer Science & Software Engineering
# The University of Western Australia
# pk at csse uwa edu au
# http://www.csse.uwa.edu.au/~pk
#
# January 2005
'''
def ridgefilter(im, orient, freq, kx, ky, showfilter):
    if im is None or orient is None or freq is None or kx is None or ky is None or showfilter is None:
        showfilter = 0

    angleInc = 3  # Fixed angle increment between filter orientations in
    # degrees. This should divide evenly into 180

    im = np.array(im, dtype=float)
    rows = im.shape[0]
    cols = im.shape[1]
    newim = np.zeros(im.shape)

    [validr, validc] = np.nonzero(freq > 0)  # find where there is valid frequency data.
    # ind = np.ravel_multi_index([rows, cols], validr, validc)
    ind = np.ravel_multi_index([validr, validc], (rows, cols))
    # Round the array of frequencies to the nearest 0.01 to reduce the
    # number of distinct frequencies we have to deal with.
    # freq[ind[0:-1]] = round(freq[ind[0:-1]] * 100) / 100
    freq[validr, validc] = np.ndarray.round(freq[validr, validc], 2)
    # Generate an array of the distinct frequencies present in the array
    # freq
    uniqufreq = np.unique(freq)

    if not uniqufreq[0]:
        uniqufreq = uniqufreq[1:]
    # Generate a table, given the frequency value multiplied by 100 to obtain
    # an integer index, returns the index within the unfreq array that it
    # corresponds to
    freqindex = np.ones(100, dtype=int)  # might need to be zeros
    for i, ele in enumerate(uniqufreq):
        index = int(round(ele * 100) - 1)
        freqindex[index] = i

    # Generate filters corresponding to these distinct frequencies and
    # orientations in 'angleInc' increments.
    filtered = np.zeros((len(uniqufreq), 180 // angleInc), dtype=np.matrix)
    sze = np.zeros(len(uniqufreq), dtype=int)

    for k, ele in enumerate(uniqufreq):
        sigmax = 1 / ele * kx
        sigmay = 1 / ele * ky

        sze[k] = round(3 * max(sigmax, sigmay))
        xarr = np.arange(-sze[k], sze[k] + 1)
        x, y = np.meshgrid(xarr, xarr)

        valEXP = np.exp(-1 * (((x ** 2) / (sigmax ** 2)) + ((y ** 2) / (sigmay ** 2))) / 2)
        valCOS = np.cos(2 * math.pi * uniqufreq[k] * x)
        reffilter = valEXP * valCOS

        ''' Generate rotated versions of the filter.  Note orientation
        # image provides orientation *along* the ridges, hence +90
        # degrees, and imrotate requires angles +ve anticlockwise, hence
        # the minus sign.'''
        for o in range(180 // angleInc):
            # img = ndimage.rotate(reffilter, -(o * angleInc + 90))  # needs to have a 'bilinear' and 'crop' implimentation
            npIm = Image.fromarray(reffilter)
            npIm = npIm.rotate(-(o * angleInc + 90), resample=Image.BILINEAR)
            rotim = np.array(npIm)
            filtered[k, o] = rotim
    if showfilter:  # Display largest scale filter for inspection
        pass  # figure(7), imshow(filter{1,},[]) title('filter')

    # Find indices of matrix points greater than maxsze from the image
    # boundary
    maxsze = sze[0]
    finalind = np.nonzero(np.logical_and(np.logical_and(validr > maxsze, validr < rows - maxsze), np.logical_and(validc > maxsze, validc < cols - maxsze)))
    # finalind = np.nonzero(maxsze < validr < rows - maxsze and maxsze < validc < cols - maxsze)

    # Convert orientation matrix values from radians to an index value
    # that corresponds to round(degrees/angleInc)
    maxorientindex = round(180 / angleInc)
    orientindex = np.array(np.round(orient / math.pi * 180 / angleInc), dtype=int)
    i = np.nonzero(orientindex < 1)
    orientindex[i] = orientindex[i] + maxorientindex
    i = np.nonzero(orientindex > maxorientindex)
    orientindex[i] = orientindex[i] - maxorientindex
    # Finally do the filtering
    for k in finalind[0]:
        r = validr[k] - 1
        c = validc[k] - 1

        # find filter corresponding to freq(r,c)
        index = int(round(freq[r, c] * 100) - 1)
        filterindex = freqindex[index]

        s = sze[filterindex - 1]
        temp1 = im[r - s:r + s + 1, c - s: c + s + 1]
        temp2 = filtered[filterindex - 1, orientindex[r, c] - 1]
        index1 = np.sum(np.sum(temp1 * temp2))
        index2 = np.sum(temp1 * temp2)
        newim[r, c] = index1
        newim[r, c] = index2

    return newim


def ridgefreq(im, mask, orient, blksze, windsze, minWaveLength, maxWaveLength):
    """
     RIDGEFREQ - Calculates a ridge frequency image

     Function to estimate the fingerprint ridge frequency across a
     fingerprint image. This is done by considering blocks of the image and
     determining a ridgecount within each block by a call to FREQEST.

     Usage:
      [freqim, medianfreq] =  ridgefreq(im, mask, orientim, blksze, windsze, ...
                                        minWaveLength, maxWaveLength)

     Arguments:
             im       - Image to be processed. should a 2D numpy array
             mask     - Mask defining ridge regions (obtained from RIDGESEGMENT) should a 2D numpy array same size as im
                            1 means part of fingerprint, 0 means background
             orientim - Ridge orientation image (obtained from RIDGORIENT) should a 2D numpy array same size as im
             blksze   - Size of image block to use (say 32). should be an int
             windsze  - Window length used to identify peaks. This should be
                        an odd integer, say 3 or 5. this should be an int
             minWaveLength,  maxWaveLength - Minimum and maximum ridge
                         wavelengths, in pixels, considered acceptable. should be int or float

     Returns:
             freqim     - An image  the same size as im with  values set to
                          the estimated ridge spatial frequency within each
                          image block.  If a  ridge frequency cannot be
                          found within a block, or cannot be found within the
                          limits set by min and max Wavlength freqim is set
                          to zeros within that block. should be 2D numpy array

             medianfreq - Median frequency value evaluated over all the
                          valid regions of the image. should be an int or float

     Suggested parameters for a 500dpi fingerprint image
       [freqim, medianfreq] = ridgefreq(im,orientim, 32, 5, 5, 15)

     I seem to find that the median frequency value is more useful as an
     input to RIDGEFILTER than the more detailed freqim.  This is possibly
     due to deficiencies in FREQEST.

     See also: RIDGEORIENT, FREQEST, RIDGESEGMENT

     Reference:
     Hong, L., Wan, Y., and Jain, A. K. Fingerprint image enhancement:
     Algorithm and performance evaluation. IEEE Transactions on Pattern
     Analysis and Machine Intelligence 20, 8 (1998), 777 789.

     Peter Kovesi
     School of Computer Science & Software Engineering
     The University of Western Australia
     pk at csse uwa edu au
     http://www.csse.uwa.edu.au/~pk

     January 2005
    """

    im = np.array(im)
    rows = im.shape[0]
    cols = im.shape[1]
    freq = np.zeros(im.shape)

    for r in range(0, rows - blksze, blksze):
        for c in range(0, cols - blksze, blksze):
            blkim = im[r:r + blksze, c: c + blksze]
            blkor = orient[r:r + blksze, c: c + blksze]
            freq[r: r + blksze, c:c + blksze] = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)

    # Mask out frequencies calculated for non ridge regions
    mask = np.array(mask)
    freq = freq * mask

    # Find median freqency over all the valid regions of the image.
    medianfreq = np.median(freq[np.nonzero(freq > 0)])

    return freq, medianfreq


def ridgeorient(im, gradientsigma, blocksigma, orientsmoothsigma):
    # Calculate image gradients. # DENNIS WROTE THIS
    Gx = derivative7(gaussFilt(im, 7, 7, gradientsigma), 'x')
    Gy = derivative7(gaussFilt(im, 7, 7, gradientsigma), 'y')

    # Estimate the local ridge orientation at each point by finding the
    # principal axis of variation in the image gradients.
    Gxx = Gx ** 2  # Covariance data for the image gradients
    Gxy = Gx * Gy
    Gyy = Gy ** 2

    # Now smooth the covariance data to perform a weighted summation of the
    # data.
    sze = math.floor(6 * blocksigma)
    if sze % 2 == 0:
        sze += 1
    Gxx = gaussFilt(Gxx, sze, sze, blocksigma)
    Gxy = 2 * gaussFilt(Gxy, sze, sze, blocksigma)
    Gyy = gaussFilt(Gyy, sze, sze, blocksigma)

    # Analytic solution of principal direction
    denom = np.sqrt(Gxy * Gxy + (Gxx - Gyy) * (Gxx - Gyy)) + np.finfo(float).eps
    sin2theta = Gxy / denom  # Sine and cosine of doubled angles
    cos2theta = (Gxx - Gyy) / denom

    if orientsmoothsigma:
        sze = math.floor(6 * orientsmoothsigma)
        if sze % 2 == 0:
            sze = sze + 1
        cos2theta = gaussFilt(cos2theta, sze, sze, orientsmoothsigma)
        sin2theta = gaussFilt(sin2theta, sze, sze, orientsmoothsigma)

    orientim = math.pi / 2.0 + np.arctan2(sin2theta, cos2theta) / 2.0
    # END HERE
    # Calculate 'reliability' of orientation data.  Here we calculate the area
    # moment about the orientation axis found (this will be the minimum moment)
    # and an axis perpendicular (which will be the maximum moment).  The
    # reliability measure is given by 1.0-min_moment/max_moment.  The reasoning
    # being that if the ratio of the minimum to maximum moments is close to one
    # we have little orientation information.

    Imin = (Gyy + Gxx) / 2 - (Gxx - Gyy) * cos2theta / 2 - Gxy * sin2theta / 2
    Imax = Gyy + Gxx - Imin

    reliability = 1 - Imin / (Imax + .001)
    coherence = ((Imax - Imin) / (Imax + Imin)) ** 2

    # Finally mask reliability to exclude regions where the denominator
    # in the orientation calculation above was small.  Here I have set
    # the value to 0.001, adjust this if you feel the need
    reliability = reliability * (denom > .001)

    return orientim, reliability, coherence


def ridgeSegment(im):
    """
    Constructs and returns a segmentation mask that identifies the fingerprint
    from the background in the image.

    :param im: The image to segment
    :return: A segmentation mask identifying the fingerprint from the background
    """
    size = im.shape

    # Error Checking
    if len(size) != 2:
        print("Image must be a 2D array")
    elif size[0] <= 1 or size[1] <= 1:
        print("Image cannot be empty")

    # Apply Median Filtering
    im = medFilt2D(im)
    im = medFilt2D(im)
    im = medFilt2D(im)
    im = medFilt2D(im)

    # Calculate the standard deveiation
    stdev = stdBlocKProc2d(im, 5, 5)
    stdev = stdev + stdBlocKProc2d(im, 10, 10)
    stdev = stdev + stdBlocKProc2d(im, 15, 15)
    stdev = stdev / 3

    # Apply Averaging Filter
    stdev = uniform_filter(stdev, size=5, mode='constant')
    stdev = uniform_filter(stdev, size=10, mode='constant')
    stdev = uniform_filter(stdev, size=30, mode='constant')

    # Apply Threshold to image
    segMask = stdev > 0.1

    return segMask


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
