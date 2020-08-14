# -*- coding: utf-8 -*-
"""transfer learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1emy8p9nejHe5oCnwJL9WQlxGNQ_ucU9d
"""

# Commented out IPython magic to ensure Python compatibility.
#Importing all the libraries
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import keras
import os
from google.colab import drive
import cv2
import random
import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import warnings
warnings.filterwarnings("ignore")

#Using google colab
drive.mount('/content/gdrive')

# Using transfer learning on pre trained model from imagenet
from keras.applications import InceptionResNetV2
conv_base = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(150,150,3))

DIR='/content/gdrive/My Drive/Household Image/'   #directory in my drive
X=[] #train data
Y=[] #Its label
files=[i+str('/')+img_dir for i in os.listdir(DIR) for img_dir in os.listdir(DIR+f'{i}')]
random.shuffle(files)       #shuffling the data
for i in files:
    print(i)
    img = cv2.imread(DIR+i,1)
    img= cv2.resize(img, (150,150))   #resizing optimum size
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    X.append(img)
    if 'Status A' in i:
        Y.append(1)
    else:
        Y.append(0)

x=np.array(X)    #all the image data after pre processing
y=np.array(Y)     # labels for each house

# VAlidation datasets obtain by randomizing the original data
X_val=[]
Y_val=[]
files=[i+str('/')+img_dir for i in os.listdir(DIR) for img_dir in os.listdir(DIR+f'{i}')]
random.shuffle(files)
for i in files:
    print(i)
    img = cv2.imread(DIR+i,1)
    img= cv2.resize(img, (150,150))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    X_val.append(img)
    if 'Status A' in i:
        Y_val.append(1)
    else:
        Y_val.append(0)

x_val=np.array(X_val)
y_val=np.array(Y_val)

#rescaling the data
train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

train_generator = train_datagen.flow(x,y)

#rescaling the validation data
val_datagen = ImageDataGenerator(rescale=1./255)

val_generator = val_datagen.flow(x_val, y_val,)

# training on pre trained model only the last fully connected layer
model = Sequential()
model.add(conv_base)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(.5))              #drophttps://www.youtube.com/watch?v=BKqUiG-ewMAout since less data leads to overfitting 
model.add(Dense(1, activation='sigmoid'))


conv_base.trainable = False
print('Number of trainable weights after freezing the conv base:', len(model.trainable_weights))

#Compiling the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

history = model.fit_generator(train_generator,
                              steps_per_epoch=40,
                              epochs=25,
                              validation_data=val_generator,
                              validation_steps=40)

#get the details form the history object
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

#Train and validation accuracy
plt.plot(epochs, acc, 'b', label='Training accurarcy')
plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
plt.title('Training and Validation accurarcy')
plt.legend()

plt.figure()
#Train and validation loss
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()

plt.show()