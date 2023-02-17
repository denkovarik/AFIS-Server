# This file runs manual tests for the feature extraction module. This script 
# can be run from the project root directory or the testing directory.
#
# Usage:
#   python3 testFeatureExtraction.py


import io
import os,sys,inspect
import numpy as np
import matplotlib.pyplot as plt
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir+'/source/pythonScripts/imEnhancement')
from imEnhancementFunctions import enhanceFingerprintImage
sys.path.insert(0, parentdir+'/source/pythonScripts/featureExtration')
from featureExtraction import *
sys.path.insert(0, parentdir+'/source/pythonScripts/tensorflowNN')
#from applyTensorflow import applyNetToValidateMinutiae
from PIL import Image, ImageOps, ImageMath
import os
import matplotlib.pyplot as plt


###############################################################################
# Testing Helper Functions
###############################################################################
def runTest(filepath):
    outDir = parentdir + "/testing/manualTests/featureExtraction/testOutput/"
    IM = Image.open(filepath)
    print("\tPerforming Image Enhancement")
    enhanced_img, unthinned_img, segmentation_mask = enhanceFingerprintImage(IM)
    enhanced_img.save(outDir + "enhanced_img.jpg", "JPEG")
    Image.fromarray(unthinned_img).save(outDir + "unthinned_img.jpg", "JPEG")
    Image.fromarray(segmentation_mask).save(outDir + "seg_mask.jpg", "JPEG")

    # convert the image to a skeleton image
    sk_img = convertImage(unthinned_img)

    # id the features
    print("\tPerforming Feature Extraction")
    features = findFeatures(sk_img, unthinned_img, segmentation_mask)
    #print("\tUsing Neural Network to limit false mintuaie")
    #features = applyNetToValidateMinutiae(enhanced_img, features)
    
    # display the image w/ minutia marked for visual verification
    #plotFeatures(sk_img, features, "Image Features")
    print("\tPlotting Features and Displaying Image")
    plotFeatures(np.invert(unthinned_img), features, "Image Features")

    # write the features to a file
    path_parts = os.path.split(filepath)
    img_name = (path_parts[-1].split('.'))[0]
    fout = open(outDir + img_name + ".xyt", "w")
    for f in features:
        x, y = f.loc()

        # fix y so that y = 0 is at the bottom
        y = unthinned_img.shape[0] - y - 1

        # output the feature data
        fout.write(str(x) + " " + str(unthinned_img.shape[0] - y - 1) + " " \
            + str(f.degrees()) + "\n")

    fout.close()
    print()


def main():
    ############################################################################
    # Test Cases
    ############################################################################
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


    ############################################################################
    # Run Test Cases
    ############################################################################
    # Just running 2 test cases for brevity. 
    # Test Case 1
    filepath = parentdir + testIm1
    foldersAndImName = filepath.split("/")
    imName = foldersAndImName[len(foldersAndImName)-1]
    print("Running test for " + imName)
    runTest(filepath)

    # Test Case 5
    filepath = parentdir + testIm5
    foldersAndImName = filepath.split("/")
    imName = foldersAndImName[len(foldersAndImName)-1]
    print("Running test for " + imName)
    runTest(filepath)


if __name__ == '__main__':
    main()
