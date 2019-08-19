# -*- coding: utf-8 -*-
"""cat_and_dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16E22wsZAHx_AxrpyRkxFY3DydbfrfKb2
"""

!wget --no-check-certificate \
  https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip \
  -O /tmp/cats_and_dogs_filtered.zip

import os
import zipfile
local_zip='/tmp/cats_and_dogs_filtered.zip'
a=zipfile.ZipFile(local_zip,'r')
a.extractall('/tmp')
a.close()

base_dir='/tmp/cats_and_dogs_filtered'
train_dir=os.path.join(base_dir,'train')
validation_dir='/tmp/cats_and_dogs_filtered/validation'
train_cat_dir=os.path.join(train_dir,'cats')
train_dog_dir=os.path.join(train_dir,'dogs')
validation_cat_dir='/tmp/cats_and_dogs_filtered/validation/cats'
validation_dog_dir='/tmp/cats_and_dogs_filtered/validation/dogs'
train_cat_name=os.listdir(train_cat_dir)
train_dog_name=os.listdir(train_dog_dir)
print(len(train_cat_name))
print(len(train_dog_name))
print(len(os.listdir(validation_cat_dir)))
print(len(os.listdir(validation_dog_dir)))

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
n_rows=4
n_cols=4
pic_index=0
fig=plt.gcf()
fig.set_size_inches(n_rows*4,n_cols*4)
pic_index+=8
next_dog=[os.path.join(train_dog_dir,fname) for fname in train_dog_name[pic_index-8:pic_index]]
next_cat=[os.path.join(train_cat_dir,fname)  for fname in train_cat_name[pic_index-8:pic_index]]
for i,img_path in enumerate(next_dog+next_cat):
  plt.subplot(n_rows,n_cols,i+1)
  img=mpimg.imread(img_path)
  plt.imshow(img)
plt.show()

import tensorflow as tf
from tensorflow import  keras
model=keras.models.Sequential([keras.layers.Conv2D(16,(3,3), activation='relu' , input_shape=(150,150,3)),
                              keras.layers.MaxPooling2D(2,2),
                              keras.layers.Conv2D(32,(3,3),activation='relu'),
                              keras.layers.MaxPooling2D(2,2),
                              keras.layers.Conv2D(64,(3,3),activation='relu'),
                              keras.layers.Flatten(),
                              keras.layers.Dense(128,activation='relu'),
                              keras.layers.Dense(1,activation='sigmoid')])

from tensorflow.keras.optimizers import RMSprop

model.compile(optimizer=RMSprop(lr=0.001),
              loss='binary_crossentropy',
              metrics = ['acc'])

from keras.preprocessing.image import ImageDataGenerator
train_datagen=ImageDataGenerator(rescale=1.0/255)
test_datagen=ImageDataGenerator(rescale=1.0/255)
trainingset=train_datagen.flow_from_directory(train_dir,
                                                batch_size=20,
                                                class_mode='binary',
                                                target_size=(150,150)
                                               )
validationset=test_datagen.flow_from_directory(validation_dir,
                                              batch_size=20,
                                              class_mode='binary',
                                              target_size=(150,150))

history=model.fit_generator(trainingset,
                           validation_data=validationset,
                           steps_per_epoch =100,
                           epochs=15,
                           validation_steps=50,
                           verbose=2)

import numpy as np
from google.colab import files
from keras.preprocessing import image

uploaded = files.upload()
for fn in uploaded.keys():
  path='/content/'+fn
  img=image.load_img(path,target_size=(150,150))
  x=image.img_to_array(img)
  x=np.expand_dims(x,axis=0)
  images=np.vstack([x])
classes=model.predict(images,batch_size=10)
if classes[0]>0:
  print(fn+"is a dog")
else:
  print(fn+"is a cat")