# -*- coding: utf-8 -*-
"""ResNet50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HeL7DFEmADVJ0RInHBdBBqYMKmsJRlVi
"""

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
import matplotlib.pyplot as plt

base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(512, 512, 3))

model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(4, activation='softmax'))

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input, rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
valid_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

# change data directory 

train_generator = train_datagen.flow_from_directory("~/G077-Machine-Leaning-Practical/Data/Clean_data/train", target_size=(512, 512), batch_size=32, class_mode='categorical')
valid_generator = valid_datagen.flow_from_directory("~/G077-Machine-Leaning-Practical/Data/Clean_data/validation", target_size=(512, 512), batch_size=32, class_mode='categorical')

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_dir = "//G077-Machine-Leaning-Practical/Data/Clean_data/test"
batch_size =32
test_generator = test_datagen.flow_from_directory(test_dir, target_size=(512, 512), batch_size=batch_size, class_mode='categorical', shuffle=False)

history = model.fit(train_generator, epochs=10, validation_data=valid_generator)

train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
print(f'Train accuracy: {train_acc * 100:.2f}%')
print(f'Validation accuracy: {val_acc * 100:.2f}%')

test_loss, test_accuracy = model.evaluate(test_generator)
print(f'Test accuracy: {test_accuracy * 100:.2f}%')
print(f'Test loss: {test_loss * 100:.2f}%')