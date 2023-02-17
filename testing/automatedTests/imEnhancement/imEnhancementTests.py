# This file runs test for the image enhancement fuctions located in 
# source/pythonScripts/imEnhancement/imEnhancementFunctions.py. This script can be
# run from the project root directory or the testing directory.
#
# Usage:
#   python3 imEnhancementTests.py 


import io
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir+'/source/pythonScripts/imEnhancement')
import numpy as np
import unittest 
import math
from PIL import Image
from imEnhancementFunctions import *
from testCases.derivative7TestCases import *
from testCases.gaussFiltTestCases import *
from testCases.ordfilt2TestCases import *
from testCases.ridgeorientTestCases import *
from testCases.imRotateTestCases import *
from testCases.freqestTestCases import *
from testCases.ridgefreqTestCases import *
from testCases.normalizeTestCases import *
from testCases.medFilt2DTestCases import *

  
class TestImEnhancementFuncs(unittest.TestCase):

    def test_isDarkRidgesOnWhite(self):
        """
        This function tests the function 'isDarkRidgesOnWhite()' on its ability 
        to determine if the fingerprint image is such that the ridges of the 
        fingerprint are dark while the background is comparatively light in color.
        """
        # Test Case 1: Image is Dark on white
        testImPath1 = parentdir + "/testing/images/MOLF/DB1_Lumidgm/jpg/100_1_1.jpg"
        im = Image.open(testImPath1)
        # Get the height and width of the image
        orgiImWidth, orgiImHeight = im.size
        aspectRatio = orgiImWidth / orgiImHeight
        # Resize the Image
        newImHeight = 500
        newImWidth = int(newImHeight * aspectRatio)
        resizedIm = im.resize((newImWidth, newImHeight))
        # Convert to grayscale
        grayIm = ImageOps.grayscale(resizedIm)
        arrIm = np.array(grayIm)
        # Normalize the Image
        normim = normalize(arrIm, 0, 1)
        # Segment the Image
        segMask = ridgeSegment(arrIm)
        self.assertTrue(isDarkRidgesOnWhite(arrIm, segMask))
        im.close()

        # Test Case 2: Image is white on dark
        testImPath1 = parentdir + "/testing/images/Nanoparticle_Images/1532_1.tif"
        im = Image.open(testImPath1)
        # Get the height and width of the image
        orgiImWidth, orgiImHeight = im.size
        aspectRatio = orgiImWidth / orgiImHeight
        # Resize the Image
        newImHeight = 500
        newImWidth = int(newImHeight * aspectRatio)
        resizedIm = im.resize((newImWidth, newImHeight))
        # Convert to grayscale
        grayIm = ImageOps.grayscale(resizedIm)
        arrIm = np.array(grayIm)
        # Normalize the Image
        normim = normalize(arrIm, 0, 1)
        # Segment the Image
        segMask = ridgeSegment(arrIm)
        self.assertTrue(not isDarkRidgesOnWhite(arrIm, segMask))
        im.close()

    
    def test_normalize(self):
        im = normalizeTest1Im
        sol = normalizeTest1Sol1
        normim = normalize(im, 0, 1)
        self.assertTrue(np.allclose(normim, sol, 0.001))


    def test_medFilt2D(self):
        im = medFilt2DTest1Im
        sol = medFilt2DTest1Sol1Im
        medIm = medFilt2D(im)
        self.assertTrue(np.allclose(medIm, sol, 0.001))


    def test_derivative7(self):
        """
        Tests the ability of derivative7() to compute the 1st derivatives of 
        an image.
        """
        # test derivative7 with respect to the x dimension
        funcansx = derivative7(derivative7Test1, 'x')
        self.assertTrue(np.allclose(funcansx, derivative7Test1Solx, 0.001))
        
        # test derivative7 with respect to the y dimension
        funcansy = derivative7(derivative7Test1, 'y')
        self.assertTrue(np.allclose(funcansy, derivative7Test1Soly, 0.001))


    def test_gaussFilt(self):
        """
        Tests the ability of gaussFilt() to apply gaussian filtering to an 
        image.
        """
        # Test case 1
        sigma = 1
        height = 7
        width = 7
        algoAns1 = gaussFilt(gaussFiltTest1, height, width, sigma) 
        self.assertTrue(np.allclose(algoAns1, gaussFiltTest1Sol, 0.001))

        # Test case 2
        sigma = 5
        height = 31
        width = 31
        algoAns2 = gaussFilt(gaussFiltTest2, height, width, sigma) 
        self.assertTrue(np.allclose(algoAns2, gaussFiltTest2Sol1, 0.001))

        # Test case 7
        sigma = 1
        height = 31
        width = 31
        algoAns3 = gaussFilt(gaussFiltTest2, height, width, sigma) 
        self.assertTrue(np.allclose(algoAns3, gaussFiltTest2Sol2, 0.001))

        
    def test_ordfilt2(self):
        """
        Tests the wrapper function for ordfilt2.
        """
        # Test Case #1
        windsze = windszeOrdfiltTest1
        proj = projOrdfilt2Test1
        sol = solOrdfiltTest1
        dilation = ordfilt2(proj, windsze, np.ones(shape=((1,windsze))))
        self.assertTrue(np.allclose(dilation, sol, 0.001))

        # Test Case #2
        windsze = windszeOrdfiltTest2
        proj = projOrdfilt2Test2
        sol = solOrdfiltTest2
        dilation = ordfilt2(proj, windsze, np.ones(shape=((1,windsze))))
        self.assertTrue(np.allclose(dilation, sol, 0.001))

        # Test Case #3
        windsze = windszeOrdfiltTest3
        proj = projOrdfilt2Test3
        sol = solOrdfiltTest3
        dilation = ordfilt2(proj, windsze, np.ones(shape=((1,windsze))))
        self.assertTrue(np.allclose(dilation, sol, 0.001))

        # Test Case #4
        windsze = windszeOrdfiltTest4
        proj = projOrdfilt2Test4
        sol = solOrdfiltTest4
        dilation = ordfilt2(proj, windsze, np.ones(shape=((1,windsze))))
        self.assertTrue(np.allclose(dilation, sol, 0.001))

        # Test Case #5
        windsze = windszeOrdfiltTest5
        proj = projOrdfilt2Test5
        sol = solOrdfiltTest5
        dilation = ordfilt2(proj, windsze, np.ones(shape=((1,windsze))))
        self.assertTrue(np.allclose(dilation, sol, 0.001))

        # Test Case #6
        windsze = windszeOrdfiltTest6
        proj = projOrdfilt2Test6
        sol = solOrdfiltTest6
        dilation = ordfilt2(proj, windsze, np.ones(shape=((1,windsze))))
        self.assertTrue(np.allclose(dilation, sol, 0.001))


    def test_ridgeorient(self):
        """
        Tests the ridgeorient function
        """
        # Test case #1
        gradientsigma = ridgeorientGradientSigma
        blocksigma = ridgeorientBlockSigma
        orientsmoothsigma = rigeorientOrientsmoothsigma
        im = ridgeorientTest1
        sol =  ridgeorientSolTest1 
        orientim, trash, trash = ridgeorient(im, 1, 5, 5)
        self.assertTrue(np.allclose(orientim, sol, atol=0.0001))
        
        # Test case #2
        gradientsigma = ridgeorientGradientSigma
        blocksigma = ridgeorientBlockSigma
        orientsmoothsigma = rigeorientOrientsmoothsigma
        im = ridgeorientTest2
        sol =  ridgeorientSolTest2
        orientim, trash, trash = ridgeorient(im, 1, 5, 5)
        self.assertTrue(np.allclose(orientim, sol, atol=0.0001))
    

    def test_imRotate(self):
        """
        Tests the wrapper function imRotate
        """
        # Test Case 1
        im = imRotateTest1
        sol = imRotateTest1Sol1
        orient = imRotateOrientTest1
        rotim = imRotate(im,orient)
        self.assertTrue(np.allclose(rotim, sol, atol=0.0001))

        # Test Case 2
        im = imRotateTest2
        sol = imRotateTest2Sol1
        orient = imRotateOrientTest2
        rotim = imRotate(im,orient)
        self.assertTrue(np.allclose(rotim, sol, atol=0.0001))

        # Test Case 3
        im = imRotateTest3
        sol = imRotateTest3Sol1
        orient = imRotateOrientTest3
        rotim = imRotate(im,orient)
        self.assertTrue(np.allclose(rotim, sol, atol=0.0001))

        # Test Case 4
        im = imRotateTest4
        sol = imRotateTest4Sol1
        orient = imRotateOrientTest4
        rotim = imRotate(im,orient)
        self.assertTrue(np.allclose(rotim, sol, atol=0.0001))


    def test_frequest(self):
        """
        Tests the image enhancement function frequests
        """
        # Test Case 1
        windsze = freqestTest1windsze
        minWaveLength = freqestTest1MinWaveLength
        maxWaveLength = freqestTest1MaxWaveLength
        blkim = freqestTest1Blkim
        blkor = freqestTest1Blkor
        sol = freqestTest1Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))

        # Test Case 2
        windsze = freqestTest2windsze
        minWaveLength = freqestTest2MinWaveLength
        maxWaveLength = freqestTest2MaxWaveLength
        blkim = freqestTest2Blkim
        blkor = freqestTest2Blkor
        sol = freqestTest2Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 3
        windsze = freqestTest3windsze
        minWaveLength = freqestTest3MinWaveLength
        maxWaveLength = freqestTest3MaxWaveLength
        blkim = freqestTest3Blkim
        blkor = freqestTest3Blkor
        sol = freqestTest3Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 4
        windsze = freqestTest4windsze
        minWaveLength = freqestTest4MinWaveLength
        maxWaveLength = freqestTest4MaxWaveLength
        blkim = freqestTest4Blkim
        blkor = freqestTest4Blkor
        sol = freqestTest4Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 5
        windsze = freqestTest5windsze
        minWaveLength = freqestTest5MinWaveLength
        maxWaveLength = freqestTest5MaxWaveLength
        blkim = freqestTest5Blkim
        blkor = freqestTest5Blkor
        sol = freqestTest5Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 6
        windsze = freqestTest6windsze
        minWaveLength = freqestTest6MinWaveLength
        maxWaveLength = freqestTest6MaxWaveLength
        blkim = freqestTest6Blkim
        blkor = freqestTest6Blkor
        sol = freqestTest6Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 7
        windsze = freqestTest7windsze
        minWaveLength = freqestTest7MinWaveLength
        maxWaveLength = freqestTest7MaxWaveLength
        blkim = freqestTest7Blkim
        blkor = freqestTest7Blkor
        sol = freqestTest7Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 8
        windsze = freqestTest8windsze
        minWaveLength = freqestTest8MinWaveLength
        maxWaveLength = freqestTest8MaxWaveLength
        blkim = freqestTest8Blkim
        blkor = freqestTest8Blkor
        sol = freqestTest8Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 9
        windsze = freqestTest9windsze
        minWaveLength = freqestTest9MinWaveLength
        maxWaveLength = freqestTest9MaxWaveLength
        blkim = freqestTest9Blkim
        blkor = freqestTest9Blkor
        sol = freqestTest9Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 10
        windsze = freqestTest10windsze
        minWaveLength = freqestTest10MinWaveLength
        maxWaveLength = freqestTest10MaxWaveLength
        blkim = freqestTest10Blkim
        blkor = freqestTest10Blkor
        sol = freqestTest10Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 11
        windsze = freqestTest11windsze
        minWaveLength = freqestTest11MinWaveLength
        maxWaveLength = freqestTest11MaxWaveLength
        blkim = freqestTest11Blkim
        blkor = freqestTest11Blkor
        sol = freqestTest11Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 12
        windsze = freqestTest12windsze
        minWaveLength = freqestTest12MinWaveLength
        maxWaveLength = freqestTest12MaxWaveLength
        blkim = freqestTest12Blkim
        blkor = freqestTest12Blkor
        sol = freqestTest12Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 13
        windsze = freqestTest13windsze
        minWaveLength = freqestTest13MinWaveLength
        maxWaveLength = freqestTest13MaxWaveLength
        blkim = freqestTest13Blkim
        blkor = freqestTest13Blkor
        sol = freqestTest13Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 14
        windsze = freqestTest14windsze
        minWaveLength = freqestTest14MinWaveLength
        maxWaveLength = freqestTest14MaxWaveLength
        blkim = freqestTest14Blkim
        blkor = freqestTest14Blkor
        sol = freqestTest14Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 15
        windsze = freqestTest15windsze
        minWaveLength = freqestTest15MinWaveLength
        maxWaveLength = freqestTest15MaxWaveLength
        blkim = freqestTest15Blkim
        blkor = freqestTest15Blkor
        sol = freqestTest15Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 16
        windsze = freqestTest16windsze
        minWaveLength = freqestTest16MinWaveLength
        maxWaveLength = freqestTest16MaxWaveLength
        blkim = freqestTest16Blkim
        blkor = freqestTest16Blkor
        sol = freqestTest16Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 17
        windsze = freqestTest17windsze
        minWaveLength = freqestTest17MinWaveLength
        maxWaveLength = freqestTest17MaxWaveLength
        blkim = freqestTest17Blkim
        blkor = freqestTest17Blkor
        sol = freqestTest17Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 18
        windsze = freqestTest18windsze
        minWaveLength = freqestTest18MinWaveLength
        maxWaveLength = freqestTest18MaxWaveLength
        blkim = freqestTest18Blkim
        blkor = freqestTest18Blkor
        sol = freqestTest18Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 19
        windsze = freqestTest19windsze
        minWaveLength = freqestTest19MinWaveLength
        maxWaveLength = freqestTest19MaxWaveLength
        blkim = freqestTest19Blkim
        blkor = freqestTest19Blkor
        sol = freqestTest19Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 20
        windsze = freqestTest20windsze
        minWaveLength = freqestTest20MinWaveLength
        maxWaveLength = freqestTest20MaxWaveLength
        blkim = freqestTest20Blkim
        blkor = freqestTest20Blkor
        sol = freqestTest20Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 21
        windsze = freqestTest21windsze
        minWaveLength = freqestTest21MinWaveLength
        maxWaveLength = freqestTest21MaxWaveLength
        blkim = freqestTest21Blkim
        blkor = freqestTest21Blkor
        sol = freqestTest21Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 22
        windsze = freqestTest22windsze
        minWaveLength = freqestTest22MinWaveLength
        maxWaveLength = freqestTest22MaxWaveLength
        blkim = freqestTest22Blkim
        blkor = freqestTest22Blkor
        sol = freqestTest22Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 23
        windsze = freqestTest23windsze
        minWaveLength = freqestTest23MinWaveLength
        maxWaveLength = freqestTest23MaxWaveLength
        blkim = freqestTest23Blkim
        blkor = freqestTest23Blkor
        sol = freqestTest23Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 24
        windsze = freqestTest24windsze
        minWaveLength = freqestTest24MinWaveLength
        maxWaveLength = freqestTest24MaxWaveLength
        blkim = freqestTest24Blkim
        blkor = freqestTest24Blkor
        sol = freqestTest24Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 25
        windsze = freqestTest25windsze
        minWaveLength = freqestTest25MinWaveLength
        maxWaveLength = freqestTest25MaxWaveLength
        blkim = freqestTest25Blkim
        blkor = freqestTest25Blkor
        sol = freqestTest25Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))

        # Test Case 26
        windsze = freqestTest26windsze
        minWaveLength = freqestTest26MinWaveLength
        maxWaveLength = freqestTest26MaxWaveLength
        blkim = freqestTest26Blkim
        blkor = freqestTest26Blkor
        sol = freqestTest26Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
       
        # Test Case 27
        windsze = freqestTest27windsze
        minWaveLength = freqestTest27MinWaveLength
        maxWaveLength = freqestTest27MaxWaveLength
        blkim = freqestTest27Blkim
        blkor = freqestTest27Blkor
        sol = freqestTest27Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 28
        windsze = freqestTest28windsze
        minWaveLength = freqestTest28MinWaveLength
        maxWaveLength = freqestTest28MaxWaveLength
        blkim = freqestTest28Blkim
        blkor = freqestTest28Blkor
        sol = freqestTest28Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))
        
        # Test Case 29
        windsze = freqestTest29windsze
        minWaveLength = freqestTest29MinWaveLength
        maxWaveLength = freqestTest29MaxWaveLength
        blkim = freqestTest29Blkim
        blkor = freqestTest29Blkor
        sol = freqestTest29Sol1  
        freqestIm = freqest(blkim, blkor, windsze, minWaveLength, maxWaveLength)
        self.assertTrue(np.allclose(freqestIm, sol, atol=0.0001))


if __name__ == '__main__':
    unittest.main() 
