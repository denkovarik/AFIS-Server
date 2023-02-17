import numpy as np
import os,sys,inspect
import subprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageOps, ImageMath


def applyNetToValidateMinutiae(img, features): 
    maxNumMinutiae = 140
    if len(features) >= maxNumMinutiae:
        return features
    filedir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    netPath = filedir + '/../../../NeuralNetworks/trainedNeuralNetworks/MinutiaeValidation_CNN.model'
    # Load the model
    model = tf.keras.models.load_model(netPath)
    # Get the image height and width
    imWidth, imheight = img.size

    arrIm = np.array(img)
    newArrIm = np.zeros(arrIm.shape)
    newArrIm[arrIm == True] = 255
    img = Image.fromarray(newArrIm)
    allMinutiaeProbs = []
    for i in range(len(features)): 
        x, y = features[i].loc()
        left = x - 24 
        right = left + 50
        top = y - 24
        bot = top + 50
        minutiae = img.crop((left, top, right, bot))
        arrIm = np.array(minutiae)
        batch_holder = np.zeros((2, 50, 50, 3))
        batch_holder[0, :, :, 0] = arrIm.copy()
        batch_holder[0, :, :, 1] = arrIm.copy()
        batch_holder[0, :, :, 2] = arrIm.copy()
        predictions = model.predict(batch_holder)
        minutiaeProb = [predictions[0][1], i]
        allMinutiaeProbs.append(minutiaeProb)
    allMinutiaeProbs.sort(reverse=True)
    newFeatures = []
    count = 0
    for i in range(len(allMinutiaeProbs)):
        if count < maxNumMinutiae:
            newFeatures.append(features[allMinutiaeProbs[i][1]])
            count = count + 1
  
    return newFeatures 
