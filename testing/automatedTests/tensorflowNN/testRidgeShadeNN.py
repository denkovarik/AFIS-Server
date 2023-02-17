# This file runs test for the fuctions that use the neural network trained
# with Tensorflow to determine the fingerprint image ridge shade. This
# is located in source/pythonScripts/tensorflowNN/ridgeShadeDetectNN.py. 
# This script can be run from the project root directory or the testing 
# directory.


import io
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir+'/source/pythonScripts/tensorflowNN')
import numpy as np
import unittest 
import math
from ridgeShadeDetectNN import isWhiteRidgesOnBlack
  
class TestRidgeShadeDetectNN(unittest.TestCase): 
  
    def test_ridgeShadeDetectNN(self):
        """
        Tests the Ridge Shade Detection Neural Network on its ability to 
        determine the whether the images are dark ridges on a white background
        and vice versa.
        """
        # Case #1
        # Tests that the Ridge Shade Detection Neural Network can classify 
        # png images that is obviously white ridges on black background
        imName = '1532_1.png'
        shadeTests = '/testing/images/ridgeShadeDetectTests'
        imPath = parentdir + shadeTests + '/whiteRidgesOnBlack/' + imName
        self.assertEqual(isWhiteRidgesOnBlack(imPath), 1)
 
        # Case #7 
        # Tests that the Ridge Shade Detection Neural Network can classify 
        # tif images that is obviously white ridges on black background
        imName = '1532_8.tif'
        imPath = parentdir + shadeTests + '/whiteRidgesOnBlack/' + imName
        self.assertEqual(isWhiteRidgesOnBlack(imPath), 1) 

        # Case #8 
        # Tests that the Ridge Shade Detection Neural Network can classify 
        # tif images that is obviously white ridges on black background
        imName = '1533_3.tif'
        imPath = parentdir + shadeTests + '/whiteRidgesOnBlack/' + imName
        self.assertEqual(isWhiteRidgesOnBlack(imPath), 1) 




        # Case #13
        # Tests that the Ridge Shade Detection Neural Network can classify 
        # an image that is obviously black ridges on white background
        imName = '1532_1.png'
        shadeTests = '/testing/images/ridgeShadeDetectTests'
        imPath = parentdir + shadeTests + '/blackRidgesOnWhite/' + imName
        self.assertEqual(isWhiteRidgesOnBlack(imPath), 0)  
        
        # Case #19
        # Tests that the Ridge Shade Detection Neural Network can classify 
        # png images that is obviously white ridges on black background
        imName = '1532_14.tif'
        imPath = parentdir + shadeTests + '/blackRidgesOnWhite/' + imName
        self.assertEqual(isWhiteRidgesOnBlack(imPath), 0) 
        
        # Case #
        # Tests that the Ridge Shade Detection Neural Network can classify 
        # png images that is obviously white ridges on black background
        imName = '1533_6.tif'
        imPath = parentdir + shadeTests + '/blackRidgesOnWhite/' + imName
        self.assertEqual(isWhiteRidgesOnBlack(imPath), 0) 





        # Supresses output
        #text_trap = io.StringIO() # create a text trap and redirect stdout
        #print("Text I don't want to see")
        #sys.stdout = sys.__stdout__ # now restore stdout function

        # Test for nan
        #self.assertEqual(math.isnan(pn.dotProduct(x)), math.isnan(math.nan))



if __name__ == '__main__': 
    unittest.main() 

