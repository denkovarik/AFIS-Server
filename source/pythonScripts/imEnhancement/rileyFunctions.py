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
	
def ridgeorient(im, gradientsigma, blocksigma, orientsmoothsigma):
# Calculate image gradients.
Gx, Gy = derivative7(gaussfilt(im, gradientsigma), 'x', 'y')  # DENNIS WROTE THIS

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
# f = fspecial('gaussian', sze, blocksigma) # DONT WORRY ABOUT
# Gxx = filter2(f, Gxx) # DONT WORRY ABOUT
# Gxy = 2*filter2(f, Gxy) # DONT WORRY ABOUT
# Gyy = filter2(f, Gyy) # DONT WORRY ABOUT

# Analytic solution of principal direction
denom = np.sqrt(Gxy ^ 2 + (Gxx - Gyy) ^ 2) + np.eps
sin2theta = Gxy / denom  # Sine and cosine of doubled angles
cos2theta = (Gxx - Gyy) / denom

if orientsmoothsigma:
	sze = math.floor(6*orientsmoothsigma)
	if sze % 2 == 0:
		sze = sze+1
	f = fspecial('gaussian', sze, orientsmoothsigma)
	cos2theta = filter2(f, cos2theta)  # Smoothed sine and cosine of DONT WORRY ABOUT
	sin2theta = filter2(f, sin2theta)  # doubled angles DONT WORRY ABOUT

orientim = math.pi / 2.0 + math.atan2(sin2theta, cos2theta) / 2.0
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


def freqest(im, orientim, windsze, minWaveLength, maxWaveLength):
    """
    # FREQEST - Estimate fingerprint ridge frequency within image block
    #
    # Function to estimate the fingerprint ridge frequency within a small block
    # of a fingerprint image.  This function is used by RIDGEFREQ
    #
    # Usage:
    #  freqim =  freqest(im, orientim, windsze, minWaveLength, maxWaveLength)
    #
    # Arguments:
    #         im       - Image block to be processed. A 2D numpy array
    #         orientim - Ridge orientation image of image block. A 2D numpy array, should be same size as im
    #         windsze  - Window length used to identify peaks. This should be
    #                    an odd integer, say 3 or 5.
    #         minWaveLength,  maxWaveLength - Minimum and maximum ridge
    #                     wavelengths, in pixels, considered acceptable. should be ints
    #
    # Returns:
    #         freqim    - An image block the same size as im with all values
    #                     set to the estimated ridge spatial frequency.  If a
    #                     ridge frequency cannot be found, or cannot be found
    #                     within the limits set by min and max Wavlength
    #                     freqim is set to zeros. should be a 2D numpy array of same size as im
    #
    # Suggested parameters for a 500dpi fingerprint image
    #   freqim = freqest(im,orientim, 5, 5, 15)
    #
    # See also:  RIDGEFREQ, RIDGEORIENT, RIDGESEGMENT
    #
    # Note I am not entirely satisfied with the output of this function.

    # Peter Kovesi
    # School of Computer Science & Software Engineering
    # The University of Western Australia
    # pk at csse uwa edu au
    # http://www.csse.uwa.edu.au/~pk
    #
    # January 2005
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
    rotim = ndimage.rotate(im, orient / math.pi * 180 + 90, mode='nearest')

    # Now crop the image so that the rotated image does not contain any
    # invalid regions.  This prevents the projection down the columns
    # from being mucked up.
    cropsze = math.floor(rows / math.sqrt(2))
    offset = math.floor((rows - cropsze) / 2)
    rotim = rotim[offset:offset + cropsze + 1, offset: offset + cropsze + 1]

    # Sum down the columns to get a projection of the grey values down
    # the ridges.
    proj = np.array([rotim.sum(axis=0)])

    # Find peaks in projected grey values by performing a greyscale
    # dilation and then finding where the dilation equals the original
    # values.
    dilation = ndimage.rank_filter(proj, rank=(windsze - 1), size=(1, windsze))

    maxpts = np.array((dilation == proj) & (proj > np.nanmean(proj)) * 1)
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
            freq[r: r + blksze, c: c + blksze] = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)

    # Mask out frequencies calculated for non ridge regions
    mask = np.array(mask)
    freq = freq * mask

    # Find median freqency over all the valid regions of the image.
    medianfreq = np.median(freq[np.nonzero(freq > 0)])

    return freq, medianfreq
