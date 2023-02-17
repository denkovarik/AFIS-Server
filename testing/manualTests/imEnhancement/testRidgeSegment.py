# This file runs manual tests for the the function 'ridgeSegment()' 
# located in source/pythonScripts/imEnhancement/imEnhancementFunctions.py. This 
# script can be run from the project root directory or the testing directory.
#
# Usage:
#   python3 testRidgeSegment.py 


import io
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir+'/source/pythonScripts/imEnhancement')
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from imEnhancementFunctions import *


###############################################################################
# Testing Helper Functions
###############################################################################
def preprocessImg(im):
    """
    Helper function used to preprocess a fingerprint image

    :param im: The fingerprint image to procross
    :return: The preprocessed grayscale image as a 2D numpy array
    :return: The preprocessed normalized image as a 2D numpy array
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
    return arrIm, normim


def runSegmentationTest(imPath):
    """
    Helper function to run manual segmentation tests

    :param imPath: The filepath to the test image
    :return: void
    """
    # Get the Test Image Name
    foldersAndImName = imPath.split("/")
    imName = foldersAndImName[len(foldersAndImName)-1]
    print("Testing Segmentation on: " + str(imName))
    # Open the Image
    im = Image.open(imPath)
    # Preprocess the Image
    arrIm, normim = preprocessImg(im)
    grayImg = Image.fromarray(arrIm.copy())
    # Construct a segmentation mask for the fingerprint image
    segMask2DArr = ridgeSegment(normim)
    if not isDarkRidgesOnWhite(arrIm, segMask2DArr):
        # Invert image
        grayImg = ImageOps.invert(grayImg)
        # Preprocess the Image
        arrIm, normim = preprocessImg(grayImg)
        grayImg = Image.fromarray(arrIm.copy())
        # Construct a segmentation mask for the fingerprint image
        segMask2DArr = ridgeSegment(normim)
    # Segment the Image
    arrIm[segMask2DArr == False] = 100
    # Convert back to PIL image
    segImg = Image.fromarray(arrIm)
    # Display Results
    d = ImageDraw.Draw(grayImg)
    d.text((10,10), "Original Image: " + imName, fill=(0))
    d = ImageDraw.Draw(segImg)
    d.text((10,10), "Segmented Image: " + imName, fill=(0))
    grayImg.show()
    segImg.show()
    input("\tPress Enter to continue...")
    # Close the Test image
    grayImg.close()
    segImg.close()


###############################################################################
# Run Test Cases
###############################################################################
testIm1 = "/testing/images/MOLF/DB1_Lumidgm/jpg/100_1_1.jpg"
testIm2 = "/testing/images/Nanoparticle_Images/1532_1.tif"
testIm3 = "/testing/images/Nanoparticle_Images/1532_10.tif"
testIm4 = "/testing/images/Nanoparticle_Images/1532_12.tif"
testIm5 = "/testing/images/Nanoparticle_Images/1532_13.tif"
testIm6 = "/testing/images/Nanoparticle_Images/1532_14.tif"
testIm7 = "/testing/images/Nanoparticle_Images/1532_2.tif"
testIm8 = "/testing/images/Nanoparticle_Images/1532_3.tif"
testIm9 = "/testing/images/Nanoparticle_Images/1532_6.tif"
testIm10 = "/testing/images/Nanoparticle_Images/1532_7.tif"
testIm11 = "/testing/images/Nanoparticle_Images/1532_8.tif"
testIm12 = "/testing/images/Nanoparticle_Images/1532_9.tif"
testIm13 = "/testing/images/Nanoparticle_Images/1533_2.tif"
testIm14 = "/testing/images/Nanoparticle_Images/1533_3.tif"
testIm15 = "/testing/images/Nanoparticle_Images/1533_6.tif"
testIm16 = "/testing/images/Nanoparticle_Images/Coke_Can_NIR_250.JPG"


# Test Case 1
testImPath1 = parentdir + testIm1
runSegmentationTest(testImPath1)

# Test Case 2
testImPath2 = parentdir + testIm2
runSegmentationTest(testImPath2)

# Test Case 16
testImPath16 = parentdir + testIm16
runSegmentationTest(testImPath16)
