import tensorflow as tf
import cv2
import numpy as np
import keras
import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use("Agg")


count = 7


for i in range(1,3000+1):
#1,904+1
    if i == 1000:
        count = count -1
    if i == 100:
        count = count -1
    if i == 10:
        count = count -1
    #C:/Users/bubbl/Desktop/Contest/mmWaveAI/TestData/leave
    # path = "C:/Users/bubbl/Downloads/Cropped_Images/Cropped_Images/Class4_multiple/"
    path = "C:/Users/bubbl/Desktop/Contest/mmWaveAI/TestData/near/"
    #path = "C:/Users/bubbl/Downloads/Cropped_Images/Cropped_Images/Gesture_Recording1_per_5_frame/"
    for j in range(0,count):
        path = path + "0"
    
    path = path + (str)(i)
    if not os.path.isfile(path+'.jpg'):
        continue
    img = cv2.imread(path + '.jpg')
    #print(img.shape)
    h,w = img.shape[:2]
    c_h = 224
    s = c_h/h
    w = int(w*s)
    h=c_h
    img = cv2.resize(img,(w,h))
    img = img[0:224, 0:224]  
    #print(img.shape)
    fig, axs = plt.subplots(1, 1)
                 # 裁切為正方形，符合 model 大小
    axs.imshow(img)
    axs.axis('off')
    fig.savefig(path)
    plt.close()











