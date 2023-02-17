# This python script will convert images to a .jpg  for every image located in
# 'inDir' and write the image out to 'outDir'.
#
# Usage:
#       python3 cnvrtDirIm2Jpg.py inputDir outputDir
#       python3 cnvrtDirIm2Jpg.py inputDir outputDir imgType2Cnvrt2

from processImage import *
import os
from PIL import Image, ImageOps
import wsq

# Check the number of command line arguments
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Invalid command line arguments.")
    print()
    print("Usage:")
    print("\tpython3 cnvrtDirIm2Jpg.py inputDir outputDir")
    print("\tpython3 cnvrtDirIm2Jpg.py inputDir outputDir imgType2Cnvrt2")
    exit()


inDir = sys.argv[1]
outDir = sys.argv[2]
imType = 'jpg'

# Check for file type to convert to
if len(sys.argv) == 4:
    imType = sys.argv[3]
    imType = imType.replace('.','')

# Check that image exists
if not os.path.isdir(inDir):
    print ("Input dir does not exist. Quitting")
    exit()

# Check that output dir exists
if not os.path.isdir(outDir):
    print ("Output dir does not exist. Quitting")
    exit()

for filename in os.listdir(inDir):
    IM = Image.open(inDir+filename)
    filename = filename.split(".")[0]
    print("Converting " + filename + " to ." + imType)
    IM.save(outDir+filename + "." + imType)
    IM.close()
