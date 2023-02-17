# This file runs manual tests for the the function 'enhanceFingerprintImage()' 
# located in source/pythonScripts/imEnhancement/imEnhancementFunctions.py. This 
# script can be run from the project root directory or the testing directory.
#
# Usage:
#   python3 testEnhanceFingerprintImage.py 


import io
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir+'/source/pythonScripts/imEnhancement')
import numpy as np
from PIL import Image, ImageDraw
from imEnhancementFunctions import *


###############################################################################
# Testing Helper Functions
###############################################################################
def resizeIm(orgiIm):
    # First create a copy of the image
    im = orgiIm.copy()
    # Get the height and width of the image
    orgiImWidth, orgiImHeight = im.size
    aspectRatio = orgiImWidth / orgiImHeight

    # Resize the Image
    newImHeight = 500
    newImWidth = int(newImHeight * aspectRatio)
    resizedIm = im.resize((newImWidth, newImHeight))
    return resizedIm


def runEnhanceFingerprintImageTest(imPath):
    """
    Helper function to run manual segmentation tests

    :param imPath: The filepath to the test image
    :return: void
    """
    # Get the Test Image Name
    foldersAndImName = imPath.split("/")
    imName = foldersAndImName[len(foldersAndImName)-1]
    print("Testing Image Enhancement on: " + str(imName))
    # Open the Image
    im = Image.open(imPath)
    showIm = resizeIm(im)
    showIm.show()
    # Enhance the Image
    enhancedImg, unThinnedBinaryIm, segMask = enhanceFingerprintImage(im)
    # Display Results
    d = ImageDraw.Draw(enhancedImg)
    d.text((10,10), "enhanceFingerprintImage: " + imName)
    enhancedImg.show()
    input("\tPress Enter to continue...")
    # Close the Test image
    im.close()
    enhancedImg.close()


###############################################################################
# Test Cases
###############################################################################
testIm1 = "/testing/images/MOLF/DB1_Lumidgm/jpg/100_1_1.jpg"
testIm2 = "/testing/images/MOLF/DB1_Lumidgm/jpg/100_1_10.jpg"
testIm3 = "/testing/images/MOLF/DB1_Lumidgm/jpg/16_3_8.jpg"
testIm4 = "/testing/images/MOLF/DB1_Lumidgm/jpg/23_2_6.jpg"
testIm5 = "/testing/images/Nanoparticle_Images/1532_1.tif"
testIm6 = "/testing/images/Nanoparticle_Images/1532_10.tif"
testIm7 = "/testing/images/Nanoparticle_Images/1532_12.tif"
testIm8 = "/testing/images/Nanoparticle_Images/1532_13.tif"
testIm9 = "/testing/images/Nanoparticle_Images/1532_14.tif"
testIm10 = "/testing/images/Nanoparticle_Images/1532_2.tif"
testIm11 = "/testing/images/Nanoparticle_Images/1532_3.tif"
testIm12 = "/testing/images/Nanoparticle_Images/1532_6.tif"
testIm13 = "/testing/images/Nanoparticle_Images/1532_7.tif"
testIm14 = "/testing/images/Nanoparticle_Images/1532_8.tif"
testIm15 = "/testing/images/Nanoparticle_Images/1532_9.tif"
testIm16 = "/testing/images/Nanoparticle_Images/1533_2.tif"
testIm17 = "/testing/images/Nanoparticle_Images/1533_3.tif"
testIm18 = "/testing/images/Nanoparticle_Images/1533_6.tif"



###############################################################################
# Run Test Cases
###############################################################################

# Just running 2 test cases for brevity. 

# Test Case 1: Image Enhancement on MOLF Image
testImPath = parentdir + testIm1
runEnhanceFingerprintImageTest(testImPath)

# Test Case 5: Image Enhancement on Nanoparticle Image
testImPath = parentdir + testIm5
runEnhanceFingerprintImageTest(testImPath)
