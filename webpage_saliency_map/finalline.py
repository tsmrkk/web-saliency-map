# coding: utf-8

#--------------------------------------------------------------
#
#   Python2.7系で作成 print関数などPython3.x系とずれる箇所あり
#   完全にテスト用のプログラム
#
#--------------------------------------------------------------

import cv2
import matplotlib.pyplot as plt
import pySaliencyMap
import numpy as np
#get screenshot
import os
from selenium import webdriver
#get html
import urllib
#read html
from bs4 import BeautifulSoup
import re
#use csv
import csv
import pandas as pd

# ライン取得
def getFinalLine():

    # 画像の読み込み
    img = cv2.imread("./output/saliency_map.png", 1)

    # 画像の高さ、幅を取得
    height = img.shape[0]/2
    width = 1280
    size = (int(width), int(height))
    halfImg = cv2.resize(img, size)

    # csvの読み込み
    tag_list_num = sum(1 for line in open('./working/tag_list_original.csv'))
    print(tag_list_num)

    tag_list = pd.read_csv('./working/tag_list_original.csv')
    print(tag_list)

    for i in range(tag_list_num - 1):
        if tag_list.iat[i, 0] == "id":
            start_x = int(tag_list.iat[i, 2])
            start_y = int(tag_list.iat[i, 3])
            end_x = int(tag_list.iat[i, 2]+tag_list.iat[i, 4])
            end_y = int(tag_list.iat[i, 3]+tag_list.iat[i, 5])

            print(start_x, start_y, end_x, end_y)

            if start_x <= width and start_y <= height:
                cv2.rectangle(halfImg, (start_x, start_y) , (end_x, end_y), (0, 0, 255), 3) # 赤色

        elif tag_list.iat[i, 0] == "class":
            start_x = int(tag_list.iat[i, 2])
            start_y = int(tag_list.iat[i, 3])
            end_x = int(tag_list.iat[i, 2]+tag_list.iat[i, 4])
            end_y = int(tag_list.iat[i, 3]+tag_list.iat[i, 5])

            print(start_x, start_y, end_x, end_y)

            if start_x <= width and start_y <= height:
                cv2.rectangle(halfImg, (start_x, start_y) , (end_x, end_y), (255, 0, 0), 2) # 青色

        elif tag_list.iat[i, 0] == "img":
            start_x = int(tag_list.iat[i, 2])
            start_y = int(tag_list.iat[i, 3])
            end_x = int(tag_list.iat[i, 2]+tag_list.iat[i, 4])
            end_y = int(tag_list.iat[i, 3]+tag_list.iat[i, 5])

            print(start_x, start_y, end_x, end_y)

            if start_x <= width and start_y <= height:
                cv2.rectangle(halfImg, (start_x, start_y) , (end_x, end_y), (0, 255, 0), 2) # 緑色

        elif tag_list.iat[i, 0] == "a":
            start_x = int(tag_list.iat[i, 2])
            start_y = int(tag_list.iat[i, 3])
            end_x = int(tag_list.iat[i, 2]+tag_list.iat[i, 4])
            end_y = int(tag_list.iat[i, 3]+tag_list.iat[i, 5])

            print(start_x, start_y, end_x, end_y)

            if start_x <= width and start_y <= height:
                cv2.rectangle(halfImg, (start_x, start_y) , (end_x, end_y), (255, 255, 0), 2) # 水色

        else:
            start_x = int(tag_list.iat[i, 2])
            start_y = int(tag_list.iat[i, 3])
            end_x = int(tag_list.iat[i, 2]+tag_list.iat[i, 4])
            end_y = int(tag_list.iat[i, 3]+tag_list.iat[i, 5])

            print(start_x, start_y, end_x, end_y)

            if start_x <= width and start_y <= height:
                cv2.rectangle(halfImg, (start_x, start_y) , (end_x, end_y), (0, 255, 255), 2) # 黄色


    # 画像を表示
    cv2.namedWindow("halfImg", cv2.WINDOW_NORMAL)
    cv2.imshow("halfImg", halfImg)
    cv2.imwrite("./output/final_line.png", halfImg ) #Save
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()


# main
if __name__ == '__main__':


    # get html
    getFinalLine()
