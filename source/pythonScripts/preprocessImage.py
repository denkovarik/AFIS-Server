# This script will preprocess a fingerprint image. I will open the image, 
# determine the ridge shade (light ridges on dark or vice versa), resize the
# image, and then save the image. The file extension for the input and output
# images and determined by the image file names.
#        
# Usage:
#       python3 preprocessImage.py inputImage outputImage

import os, os.path, sys,inspect
import numpy as np
from imEnhancement.imEnhancementFunctions import * 
from featureExtration.featureExtraction import *
#from tensorflowNN.applyTensorflow import applyNetToValidateMinutiae
import PIL.Image as Image
import wsq


# Check the number of command line arguments
if len(sys.argv) != 3:
    print("Invalid command line arguments.")
    print()
    print("Usage:")
    print("\tpython3 preprocessImage.py inputImage outputImage")
    exit()

filePath = os.getcwd() + "/" + sys.argv[1]
outFile = os.getcwd() + "/" + sys.argv[2]

# Check that image exists
if not os.path.isfile(filePath):
    print ("Image does not exist. Quitting")
    exit()

IM = Image.open(filePath)
IM.show()

# Get the height and width of the image
orgiImWidth, orgiImHeight = IM.size
aspectRatio = orgiImWidth / orgiImHeight

# Resize the Image
newImHeight = 500
newImWidth = int(newImHeight * aspectRatio)
IM = IM.resize((newImWidth, newImHeight))

# Convert to grayscale
IM = ImageOps.grayscale(IM)

# Convert to 2D numpy array
arrIm = np.array(IM)

# Normalize the image
normim = normalize(arrIm, 0, 1)

# Construct a segmentation mask for the fingerprint image
segMask2DArr = ridgeSegment(normim)

# Ensure Fingerprint Image is Dark on Light
if not isDarkRidgesOnWhite(arrIm, segMask2DArr):
    IM = ImageOps.invert(IM)

IM.show()
IM.save(outFile)
