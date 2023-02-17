# This python script will generate .xyt minutiae files from fingerprint images 
# located in a specified directory. For each image in a specified directory, 
# this script will perform fingerprint image enhancement on the image, extract
# the minutiae from the image, and then write the extrated minutiae to a .xyt 
# file in a format accecptable for the Bozorth3 matcher. The input directory 
# that holds the images to enhance and extract features from is specified by
# the first command line argument. The output directory to write the xyt 
# minutiae files to is specified by the second command line argument.
#
# Usage:
#       python3 genXytMinutiaeFiles.py inputDir outputDir

from processImage import *
import os, sys
from PIL import Image
import wsq

# Check the number of command line arguments
if len(sys.argv) != 3:
    print("Invalid command line arguments. Two additional arguements must be ")
    print("passed in on the command line to specify the input and output ")
    print("directories. The first command line argument specifies the ")
    print("directory containing the images to extract the minutiae from, ") 
    print("while the second specifies the output directory to write the xyt ")
    print("files to.")
    print()
    print("Usage:")
    print("\tpython3 genXytMinutiaeFiles.py inputDir outputDir")
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
    processImage(inDir+filename, outDir)
