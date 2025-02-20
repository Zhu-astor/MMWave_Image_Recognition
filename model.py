import tensorflow as tf
import cv2
import numpy as np
from keras.models import load_model
import keras
import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use("Agg")

print(tf.__version__)
print(keras.__version__)

model = load_model('keras_model.h5', compile=False)   # 載入 model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)           # 設定資料陣列

count = 7

sum_100 = 299
sum_90 = 299
sum_80 = 299
sum_70 = 299
sum_60 = 299

file1 = open("Accuracy.txt","w")

for i in range(1,2371+1):
#1,904+1
    if i == 1000:
        count = count -1
    if i == 100:
        count = count -1
    if i == 10:
        count = count -1
        
    # path = "C:/Users/bubbl/Downloads/Cropped_Images/Cropped_Images/test_near/"
    path = "C:/Users/bubbl/Desktop/Contest/mmWaveAI/TestData/leave_resize/"
    #path = "C:/Users/bubbl/Downloads/Cropped_Images/Cropped_Images/Gesture_Recording1_per_5_frame/"
#     0
# 94
# 203
# 315
# 425
    for j in range(0,count):
        path = path + "0"
    
    path = path + (str)(i)
    print(path)
    
    if not os.path.isfile(path+'.png'):
        continue
    
    img = cv2.imread(path + '.png')
    h,w = img.shape[:2]
    c_h = 224
    s = c_h/h
    w = int(w*s)
    h=c_h
    img = cv2.resize(img,(w,h))
    img = img[0:224, 0:224]  
    # print(img.shape)
    fig, axs = plt.subplots(1, 1)
                 # 裁切為正方形，符合 model 大小
    
    image_array = np.asarray(img)          # 去除換行符號和結尾空白，產生文字陣列
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1  # 轉換成預測陣列
    data[0] = normalized_image_array
    prediction = model.predict(data)       # 預測結果
    # print(prediction)
    a,b,c= prediction[0]                   # 取得預測結果

    print("near ",a)
    print("leave ",b)
    print("multi ",c)
    word = ""
    if max(a,b,c) == a :    
        word = "near"
        temp = a
    elif max(a,b,c) == b:
        word = "leave"
        temp = b
    else :
        word = "multi"
        temp = c
    
    
    if a< 1 and b < 1 and c< 1:
        sum_100 = sum_100 - 1
    if a<0.9 and b <0.9 and c<0.9:
        sum_90 = sum_90 - 1
    if a<0.8 and b <0.8 and c<0.8:
        sum_80 = sum_80 - 1
    if a<0.7 and b <0.7 and c<0.7:
        sum_70 = sum_70 - 1
    if a<0.6 and b <0.6 and c<0.6:
        sum_60 = sum_60 - 1
        
    file1.write(str(i))
    file1.write("\n")
    file1.write("near: " + str(a) + "\n")
    file1.write("leave: " + str(b) + "\n")
    file1.write("multi: " + str(c) + "\n")
    file1.write("----------------------"+"\n")
    
    axs.imshow(img)
    axs.set_title(word + "%f" % temp)
    axs.axis('off')
    fig.savefig(path)
    plt.close()

    
print(sum_100)
print(sum_90)
print(sum_80)
print(sum_70)
print(sum_60)










