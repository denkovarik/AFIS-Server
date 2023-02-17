from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import os, sys, inspect

print("Training Neural Network detect if fingerprint has dark ridges on a light background or vice versa.")

filedir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
netPath = filedir + '/../../../NeuralNetworks/trainedNeuralNetworks/RidgeShadeDetection_CNN.model' 

train = ImageDataGenerator(rescale=1/255)
validation = ImageDataGenerator(rescale=1/255)

train_dataset = train.flow_from_directory(filedir + '/../../../Datasets/RidgeShadeDetection/Train/',
                                          target_size=(100,100),
                                          batch_size = 50,
                                          class_mode = 'binary')

validation_dataset = train.flow_from_directory(filedir + '/../../../Datasets/RidgeShadeDetection/Validation/',
                                          target_size=(100,100),
                                          batch_size = 50,
                                          class_mode = 'binary')

test_dataset = train.flow_from_directory(filedir + '/../../../Datasets/RidgeShadeDetection/Test/',
                                          target_size=(100,100),
                                          batch_size = 20,
                                          class_mode = 'binary')

model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(32,(3,3),activation = 'relu', input_shape = (100, 100, 3)),
                                     tf.keras.layers.MaxPool2D(2,2),
                                     tf.keras.layers.Conv2D(32,(3,3),activation = 'relu'),
                                     tf.keras.layers.MaxPool2D(2,2),
                                     tf.keras.layers.Conv2D(32,(3,3),activation = 'relu'),
                                     tf.keras.layers.MaxPool2D(2,2),
                                     tf.keras.layers.Flatten(),
                                     tf.keras.layers.Dense(512, activation = 'relu'),
                                     tf.keras.layers.Dense(2)
                                     ])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


model_fit = model.fit(train_dataset,
                      steps_per_epoch = 50,
                      epochs = 10,
                      validation_data = validation_dataset)

model.save(filedir + '/../../../NeuralNetworks/trainedNeuralNetworks/RidgeShadeDetection_CNN.model')
