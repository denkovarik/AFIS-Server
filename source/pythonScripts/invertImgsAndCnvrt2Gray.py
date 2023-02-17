# This python script will just invert and convert to grayscale every image in 
# 'inDir' and write the image out to 'outDir'
#
# Usage:
#       python3 invertImgsAndCnvrt2Gray.py inputDir outputDir

from processImage import *
import os
from PIL import Image, ImageOps
import wsq

# Check the number of command line arguments
if len(sys.argv) != 3:
    print("Invalid command line arguments. Two additional arguements must be ")
    print("passed in on the command line to specify the input and output ")
    print("directories. The first command line argument specifies the ")
    print("directory containing the images, while the second specifies the ")
    print("output directory to write the converted images to.")
    print()
    print("Usage:")
    print("\tpython3 invertImgsAndCnvrt2Gray.py inputDir outputDir")
    exit()


inDir = sys.argv[1]
outDir = sys.argv[2]

# Check that image exists
if not os.path.isdir(inDir):
    print ("Input dir does not exist. Quitting")
    exit()

# Check that output dir exists
if not os.path.isdir(outDir):
    print ("Output dir does not exist. Quitting")
    exit()

for filename in os.listdir(inDir):
    print("Processing " + filename)
    IM = Image.open(inDir+filename)
    # Convert to grayscale
    IM = ImageOps.grayscale(IM)
    # Invert colors
    IM = ImageOps.invert(IM)
    IM.save(outDir+filename.split(".")[0] + ".wsq")
