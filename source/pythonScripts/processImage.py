# This file holds the function "processImage" which acts like the main program
# for running the image enhancement and feature extraction modules on a 
# fingerprint image. Otherwise, the "main function" for this script requires
# 2 command line arguments passed in. The first is the filepath for the 
# fingerprint image to enhance and extract features from, the second is the
# directory to write the .xyt file (containing the extracted minutiae) to.
#        
# Usage:
#       python3 processImage.py inputFingerprintImage outputDir

import os, os.path, sys,inspect
import numpy as np
from imEnhancement.imEnhancementFunctions import * 
from featureExtration.featureExtraction import *
#from tensorflowNN.applyTensorflow import applyNetToValidateMinutiae
import PIL.Image as Image
import wsq


def processImage(filepath, minutiaeOutDir):
    IM = Image.open(filepath)
    print("\tPerforming Image Enhancement")
    enhanced_img, unthinned_img, segmentation_mask = enhanceFingerprintImage(IM)

    # convert the image to a skeleton image
    sk_img = convertImage(unthinned_img)

    # id the features
    print("\tPerforming Feature Extraction")
    features = findFeatures(sk_img, unthinned_img, segmentation_mask)
    #print("\tUsing Neural Network to limit false mintuaie")
    #features = applyNetToValidateMinutiae(enhanced_img, features)
    
    # display the image w/ minutia marked for visual verification
    #print("\tPlotting Features and Displaying Image")
    #plotFeatures(sk_img, features, "Image Features")
    #plotFeatures(unthinned_img, features, "Image Features")

    # write the features to a file
    print("\tWriting .xyt file")
    path_parts = os.path.split(filepath)
    img_name = (path_parts[-1].split('.'))[0]
    fout = open(minutiaeOutDir + img_name + ".xyt", "w")

    for f in features:
        x, y = f.loc()

        # fix y so that y = 0 is at the bottom
        y = unthinned_img.shape[0] - y - 1

        # output the feature data
        fout.write(str(x) + " " + str(unthinned_img.shape[0] - y - 1) + " " + str(int(f.degrees())) + "\n")

    fout.close()
    print()



if __name__ == '__main__':
    # Check the number of command line arguments
    if len(sys.argv) != 3:
        print("Invalid command line arguments. Two additional arguements must be ")
        print("passed in on the command line to specify the input fingerprint ")
        print("image and the output directory to write the .xyt file to. The ")
        print("first command line argument is the filepath for the input ")
        print("fingerprint image to enhance and extract features from, while ")
        print("the second specifies the output directory to write the xyt ")
        print("files to.")
        print()
        print("Usage:")
        print("\tpython3 processImage.py inputFingerprintImage outputDir")
        exit()

    filePath = os.getcwd() + "/" + sys.argv[1]
    outDir = os.getcwd() + "/" + sys.argv[2]

    # Check that image exists
    if not os.path.isfile(filePath):
        print ("Image does not exist. Quitting")
        exit()

    # Check that output dir exists
    if not os.path.isdir(outDir):
        print ("Output dir does not exist. Quitting")
        exit()

    processImage(filePath, outDir)
