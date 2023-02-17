# This file runs test for the fuctions that use the neural network trained
# with Tensorflow to validate minutiae. This
# is located in source/pythonScripts/tensorflowNN/validateMinutiaeNN.py. 
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
from validateMinutiaeNN import getMinutiaeProb
  
class TestValidateMinutiaeNN(unittest.TestCase): 
  
    def test_validateMinutiaeNN(self):
        """
        Tests the Ridge Shade Detection Neural Network on its ability to 
        determine the whether the images are dark ridges on a white background
        and vice versa.
        """
        # Case #1
        # Tests valid minutiae
        imName = 'validMinutiae-101_4(295,164).png'
        minutiaeTests = '/testing/images/minutiaeValidationTests'
        imPath = parentdir + minutiaeTests + '/validMinutiae/' + imName
        notMinutiaeProb, isMinutiaeProb = getMinutiaeProb(imPath)
        self.assertTrue(isMinutiaeProb > notMinutiaeProb)

        # Case #2 
        #'images/minutiaeValidationTests/invalidMinutiae/invalidMinutiae-100_R1_0(116,473).png'
        imName = 'invalidMinutiae-100_R1_0(116,473).png'
        minutiaeTests = '/testing/images/minutiaeValidationTests'
        imPath = parentdir + minutiaeTests + '/invalidMinutiae/' + imName
        notMinutiaeProb, isMinutiaeProb = getMinutiaeProb(imPath)
        self.assertTrue(isMinutiaeProb < notMinutiaeProb)

        # Supresses output
        #text_trap = io.StringIO() # create a text trap and redirect stdout
        #print("Text I don't want to see")
        #sys.stdout = sys.__stdout__ # now restore stdout function

        # Test for nan
        #self.assertEqual(math.isnan(pn.dotProduct(x)), math.isnan(math.nan))



if __name__ == '__main__': 
    unittest.main() 

