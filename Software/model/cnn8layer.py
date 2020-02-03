# -*- coding: utf-8 -*-
"""Cnn8layer.ipynb
"""
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.utils import np_utils
from datetime import datetime

class Cnn8layer():
    def __init__(self, num_rows, num_columns, num_channels, num_labels, checkpoint=None):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_channels = num_channels
        self.num_labels = num_labels
        self.checkpoint = checkpoint
        self.create_model()

    def create_model(self):
      self.model = Sequential()
      self.model.add(Conv2D(filters=32, kernel_size=2, input_shape=(self.num_rows, self.num_columns, self.num_channels), activation='relu'))
      self.model.add(Dropout(0.2))
      
      self.model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
      self.model.add(MaxPooling2D(pool_size=2))
      self.model.add(Dropout(0.2))
      
      self.model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
      self.model.add(Dropout(0.2))

      self.model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
      self.model.add(Dropout(0.2))
      
      self.model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
      self.model.add(Dropout(0.2))

      self.model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
      self.model.add(Dropout(0.2))

      self.model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
      self.model.add(Dropout(0.2))
      self.model.add(GlobalAveragePooling2D())
      
      self.model.add(Dense(self.num_labels, activation='softmax'))
      
      adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
      if self.checkpoint:
          self.model.load_weights(self.checkpoint)
          print("weights loaded from", self.checkpoint)

      self.model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=adam)
      
      # Display model architecture summary 
      self.model.summary()

    def train(self, x_train, x_test, y_train, y_test, x_val=None, y_val=None, num_epochs = 10, num_batch_size = 32, checkpoint=None):
        if not x_val:
            x_val = x_test
        if not y_val:
            y_val = y_test
        score = self.model.evaluate(x_test, y_test, verbose=1)
        accuracy = 100*score[1]

        print("Pre-training accuracy: %.4f%%" % accuracy)

        
        if checkpoint==None:
            callbacks = None
        else:
            checkpointer = ModelCheckpoint(filepath=checkpoint, verbose=1)
            callbacks = [checkpointer]

        start = datetime.now()
        self.model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), verbose=1, callbacks=callbacks)
        duration = datetime.now() - start
        print("Training completed in time: ", duration)

        score = self.model.evaluate(x_train, y_train, verbose=0)
        print("Training Accuracy:", score[1])

        score = self.model.evaluate(x_test, y_test, verbose=0)
        print("Testing Accuracy: ", score[1])

    def predict(self, x, batch_size=None):
        start = datetime.now()
        result = self.model.predict(x, batch_size=batch_size)
        duration = datetime.now() - start
        print("Prediction completed in time: ", duration)
        return result
