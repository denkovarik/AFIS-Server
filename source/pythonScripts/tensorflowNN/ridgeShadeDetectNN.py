import sys, os, inspect
import subprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow import keras
import numpy as np
import PIL
import PIL.Image
from tensorflow.keras.preprocessing import image



def isWhiteRidgesOnBlack(imPath):
    filedir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    netPath = filedir + '/../../../NeuralNetworks/trainedNeuralNetworks/RidgeShadeDetection_CNN.model' 
    
    model = tf.keras.models.load_model(netPath)

    batch_holder = np.zeros((2, 100, 100, 3))
    img = image.load_img(imPath, target_size=(100,100))
    batch_holder[0, :] = img
    predictions = model.predict(batch_holder)

    if predictions[0][1] > predictions[0][0]:
        return 1
    return 0
