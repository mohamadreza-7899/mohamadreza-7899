from keras.datasets import cifar10
from skimage import data
import numpy as np
import matplotlib.pyplot as plt


(x_train, y_train), (x_test, y_test) = cifar10.load_data()

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)



image_index = 24090
plt.imshow(x_train[image_index] , cmap = 'gray')
print('Label : ', y_train[image_index])


x_train_final = x_train.reshape(-1,32*32*3)/255
x_test_final = x_test.reshape(-1,32*32*3)/255

print(x_train_final.shape)
print(x_test_final.shape)


from keras.utils import to_categorical
y_train_cat = to_categorical(y_train,10)
y_test_cat = to_categorical(y_test,10)
print(y_train_cat.shape)
print(y_test_cat.shape)

from keras.models import Sequential
from keras.layers import Dense, Input

model = Sequential()
model.add(Input(shape = (32*32*3)))
model.add(Dense(512, activation = 'relu'))
model.add(Dense(512, activation = 'relu'))
model.add(Dense(1024, activation = 'relu'))
model.add(Dense(10 , activation = 'softmax'))


model.compile(optimizer= 'adam',loss= 'categorical_crossentropy',metrics = ['accuracy'])

model.summary()


batch_size = 128
epochs = 30

batch_size = 128
epochs = 30
model.fit(x_train_final, y_train_cat,
          batch_size= batch_size ,
          epochs=epochs, verbose= 1,
          validation_data=(x_test_final,y_test_cat))


x_train_final = x_train/ 255
x_test_final = x_test/ 255


from keras.utils import to_categorical
y_train_cat = to_categorical(y_train,10)
y_test_cat = to_categorical(y_test,10)
print(y_train_cat.shape)
print(y_test_cat.shape)


from keras.models import Sequential
from keras.layers import Dense,MaxPool2D,Flatten, Conv2D


from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D

model = Sequential()
model.add(Conv2D(filters = 32, kernel_size=(3,3), activation='relu', input_shape = (32,32,3)))
model.add(Conv2D(filters = 32, kernel_size=(3,3), activation='relu'))
model.add(Conv2D(filters = 32, kernel_size=(3,3), activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(10, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer = 'adam' , metrics = ['accuracy'])


model.summary()



batch_size = 128
epochs = 30
model.fit(x_train_final, y_train_cat,
          batch_size= batch_size ,
          epochs=epochs, verbose= 1,
          validation_data=(x_test_final,y_test_cat))


x_train_final = x_train.reshape(-1,32*32*3)/255
x_test_final = x_test.reshape(-1,32*32*3)/255

print(x_train_final.shape)
print(x_test_final.shape)

from keras.utils import to_categorical
y_train_cat = to_categorical(y_train,10)
y_test_cat = to_categorical(y_test,10)
print(y_train_cat.shape)
print(y_test_cat.shape)

from keras.models import Sequential
from keras.layers import Dense, Input
model = Sequential()
model.add(Input(shape = (32*32*3)))
model.add(Dense(2048, activation = 'relu'))
model.add(Dense(2048, activation = 'relu'))
model.add(Dense(2048, activation = 'relu'))
model.add(Dense(10 , activation = 'softmax'))

model.compile(optimizer= 'adam',loss= 'categorical_crossentropy',metrics = ['accuracy'])

model.summary()

batch_size = 128
epochs = 30
model.fit(x_train_final, y_train_cat,
          batch_size= batch_size ,
          epochs=epochs, verbose= 1,
          validation_data=(x_test_final,y_test_cat))
