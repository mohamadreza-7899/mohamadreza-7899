# -*- coding: utf-8 -*-
"""Techno Saze.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1leeCV4j-KwdQDVWcEgk8vgQuC2cF_-CD
"""

import numpy as np
import pandas as pd
import tensorflow as tf

dataset  = pd.read_csv('/content/PMRatio.csv')
#dataset = dataset.drop("c", 1)
#dataset = dataset.drop("k", 1)

dataset.head()

x = dataset.iloc[:,0:-1].values
y = dataset.iloc[:,-1].values

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(x)
X[0]

from sklearn.model_selection import train_test_split  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train

ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units= 64, activation='relu'))
ann.add(tf.keras.layers.Dense(units= 64, activation='relu'))
ann.add(tf.keras.layers.Dropout(0.2))
ann.add(tf.keras.layers.Dense(units= 16, activation='relu'))

ann.compile(optimizer='adam',loss='mean_squared_error', metrics=['mean_squared_error'])

ann.fit(X_train, y_train, batch_size = 64, epochs=500, validation_data = (X_test, y_test))