import cv2  #导入opencv模块
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
from datetime import datetime 
#%%
def count_dot(img):
#print("Hellow word!")     #打印“Hello word！”，验证模块导入成功

    #img = img.astype('uint8')
    #cv2.namedWindow("imagshow", 2)   #创建一个窗口
    #cv2.imshow('imagshow', img)    #显示原始图片

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #转换为灰度图

    #使用局部阈值的大津算法进行图像二值化
    dst = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,101, 1)

    #全局大津算法，效果较差
    #res ,dst = cv2.threshold(gray,0 ,255, cv2.THRESH_OTSU)

    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3, 3))#形态学去噪
    dst=cv2.morphologyEx(dst,cv2.MORPH_OPEN,element)  #开运算去噪

    contours, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #轮廓检测函数
    cv2.drawContours(dst,contours,-1,(120,0,0),2)  #绘制轮廓

    count=0 #米粒总数
    ares_avrg=0  #米粒平均
    #遍历找到的所有米粒
    for cont in contours:

        ares = cv2.contourArea(cont)#计算包围性状的面积

        if ares<50:   #过滤面积小于10的形状
            continue
        if ares>1000:   #过滤面积小于10的形状
            continue
        count+=1    #总体计数加1
        ares_avrg+=ares

    #    print("{}-blob:{}".format(count,ares),end="  ") #打印出每个米粒的面积

        rect = cv2.boundingRect(cont) #提取矩形坐标

    #    print("x:{} y:{}".format(rect[0],rect[1]))#打印坐标

        cv2.rectangle(img,rect,(0,0,0xff),1)#绘制矩形

        y=10 if rect[1]<10 else rect[1] #防止编号到图片之外

        cv2.putText(img,str(count), (rect[0], y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1) #在米粒左上角写上编号

    #print("米粒平均面积:{}".format(round(ares_avrg/ares,2))) #打印出每个米粒的面积

 #   cv2.namedWindow("imagshow", 2)   #创建一个窗口
  #  cv2.imshow('imagshow', img)    #显示原始图片

  #  cv2.namedWindow("dst", 2)   #创建一个窗口
   # cv2.imshow("dst", dst)  #显示灰度图
    #print(count)
    return count

    #plt.hist(gray.ravel(), 256, [0, 256]) #计算灰度直方图
    #plt.show()

   # cv2.waitKey(0)

#%%
name_list=[]
value_list = []
df=pd.DataFrame()

file_list = sorted(glob.glob("./images/*.tif"))
#print(file_list)
if not os.path.exists("./results/"):
    os.makedirs("./results/")

for file1 in file_list:
    img = cv2.imread(file1) 
    file_name = file1.split(".tif")[0].split("/")[-1]
    res=count_dot(img)
    name_list.append(file_name)
    value_list.append(res)

df["name"]=name_list
df["count"]=value_list
#print(df)
now = datetime.now() 
strnow = datetime.strftime(now,'%Y_%m_%d_%H_%M_%S')
path="./results/result_"+strnow+".xls"
df.to_excel(path)

    



