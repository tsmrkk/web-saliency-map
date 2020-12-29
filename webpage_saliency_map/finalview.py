# coding: utf-8

#--------------------------------------------------------------
#
#   Python2.7系で作成 print関数などPython3.x系とずれる箇所あり
#   出力用プログラム2018/12/10時点
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
# 画像のPIP処理
from PIL import Image

global high_element_list # 顕著度ランキングを格納するリスト

#顕著度ランキングの計算
def getHighestSaliency():

    # あとで消す！！
    screenshot = cv2.imread("./working/screen-pc.png", 1)
    height = screenshot.shape[0]/2
    width = 1280
    size = (int(width), int(height))
    screenshot = cv2.resize(screenshot, size)

    # csvの行数を取得
    tag_list_num = sum(1 for line in open('./working/tag_list_custom.csv')) - 1 #タイトルヘッダー文をマイナス
    # csvの読み込み
    tag_list = pd.read_csv('./working/tag_list_custom.csv')

    # 顕著度を格納するリスト
    salient_level = []
    # NGリスト
    ng_list = []
    # 顕著度ランキングを格納するリスト
    global high_element_list
    high_element_list = []


    # 顕著度を配列に格納
    i = 1 # タイトルの次から実行
    for i in range(tag_list_num):
        if tag_list.iat[i, 0] == "id_large" or tag_list.iat[i, 0] == "class_large":
            salient_level.append(-1)
        else:
            salient_level.append(tag_list.iat[i, 7])

    print("リスト：salient_level")
    print(salient_level)

    salient_level_sort = np.sort(salient_level)
    salient_level_sort_final = np.argsort(salient_level)
    print("リスト：salient_level_sort")
    print(salient_level_sort)
    print("リスト：salient_level_final")
    print(salient_level_sort_final)

    salient_num = 10 # 上位何個表示するか？ 10
    temporal_num = 1 # 一時的な変数
    salient_num_first = salient_num


    while salient_num > 0 :
        most_salient = salient_level_sort_final[tag_list_num - temporal_num]
        print(most_salient)
        if (most_salient in ng_list) == False:
            start_x = int(tag_list.iat[most_salient, 2])
            start_y = int(tag_list.iat[most_salient, 3])
            end_x = int(tag_list.iat[most_salient, 2]+tag_list.iat[most_salient, 4])
            end_y = int(tag_list.iat[most_salient, 3]+tag_list.iat[most_salient, 5])
            size = int(tag_list.iat[most_salient, 4]*tag_list.iat[most_salient, 5])
            if start_x < 0 :
                start_x = 0
            if start_y < 0 :
                start_y = 0
            if end_x > width:
                end_x = width
            if end_y > height:
                end_y = height

            if (end_x - start_x)/(end_y - start_y) < 10: # あまりにも細長いものを排除
                clipped = screenshot[int(start_y):int(end_y),int(start_x):int(end_x)]
                cv2.imwrite("./working/high-saliency/img"+ str(salient_num_first - salient_num + 1) +".png", clipped ) #Save
                print("画像出力 & 顕著度高いリストに追加")
                high_element_list.append(most_salient)
                salient_num -= 1

                print("%s %s %s %s 顕著度→%s" %(start_x, start_y, end_x, end_y, tag_list.iat[most_salient, 7]) )

                i = 1 # タイトルの次から実行
                for i in range(tag_list_num):
                    if (i in ng_list) == False:
                        research_start_x = int(tag_list.iat[i, 2])
                        research_start_y = int(tag_list.iat[i, 3])
                        research_end_x = int(tag_list.iat[i, 2]+tag_list.iat[i, 4])
                        research_end_y = int(tag_list.iat[i, 3]+tag_list.iat[i, 5])
                        research_size = int(tag_list.iat[most_salient, 4]*tag_list.iat[most_salient, 5])

                        if (start_x >= research_start_x) and (start_y >= research_start_y) and (end_x <= research_end_x) and (end_y <= research_end_y):
                            print("%s 番怪しい" %i)
                            if research_size - size < 200:
                                ng_list.append(i)
                                print("NGリストに %s を格納" %i)
                        elif (start_x <= research_start_x) and (start_y <= research_start_y) and (end_x >= research_end_x) and (end_y >= research_end_y):
                                print("%s 番怪しい" %i)
                                if  size - research_size < 200:
                                    ng_list.append(i)
                                    print("NGリストに %s を格納" %i)
            else:
                print("細長すぎます")
        else:
            print("NG Fileに入っています")
        temporal_num += 1

    print(high_element_list)


#最終出力
def getFinalView():

  # 画像の読み込み
  img = cv2.imread("./output/saliency_map.png", 1)
  screenshot = cv2.imread("./working/screen-pc.png", 1)

  # 画像の高さ、幅を取得
  height = img.shape[0]/2
  width = 1280
  size = (int(width), int(height))
  halfImg = cv2.resize(img, size)
  halfImg_print = cv2.resize(img, size)

  # 画像の高さ、幅を取得
  height = screenshot.shape[0]/2
  width = 1280
  size = (int(width), int(height))
  screenshot = cv2.resize(screenshot, size)


  # csvの読み込み
  tag_list_num = sum(1 for line in open('./working/tag_list_custom.csv'))
  print(tag_list_num)

  tag_list = pd.read_csv('./working/tag_list.csv')
  #print(tag_list)

  tag_list_custom = pd.read_csv('./working/tag_list_custom.csv')

  # 補正値
  correction = 20 # 20

  # 顕著度の塗りつぶし用関数
  def printSaliencyColor(i, type):
    start_x = int(tag_list_custom.iat[i, 2])
    start_y = int(tag_list_custom.iat[i, 3])
    end_x = int(tag_list_custom.iat[i, 2]+tag_list_custom.iat[i, 4])
    end_y = int(tag_list_custom.iat[i, 3]+tag_list_custom.iat[i, 5])
    salient_level_num = tag_list_custom.iat[i, 7]*10
    if type == 'img' and ((end_x - start_x)*(end_y - start_y)) / (width*height) > 0.1 :
      # 画像の場合のみそのまま貼り付け
      # memo どちらか一片の長さが64pxを超える画像はそのまま顕著性マップを表示するように修正する
      # ただし、現状として画像の取得を確実にできていないように思えるためその箇所を検証後実装する
      if start_x < 0 or start_y < 0 or end_x > width or end_y > height:
        return

      clipped = halfImg[start_y:end_y,start_x:end_x]
      print(clipped.shape)
      print(halfImg_print.shape)
      print(start_x, start_y)
      halfImg_print[start_y:clipped.shape[0] + start_y, start_x:clipped.shape[1] + start_x] = clipped
    else :
      if salient_level_num > 0:
        cv2.rectangle(halfImg_print, (start_x, start_y) , (end_x, end_y), (salient_level_num + correction, salient_level_num + correction, salient_level_num + correction), -1)



  # 配列のソート
  element_area_list = []
  for i in range(tag_list_num - 1):
    element_area_list.append(int(tag_list_custom.iat[i, 8]))
  element_area_lank_sorted_index = np.argsort(element_area_list)[::-1]

  print(element_area_list)
  print(element_area_lank_sorted_index)

  for i in element_area_lank_sorted_index:
    print(tag_list_custom.iat[i, 1])
    if tag_list_custom.iat[i, 0] == "id" or tag_list.iat[i, 0] == "id_large":
      printSaliencyColor(i, 'id')
    elif tag_list_custom.iat[i, 0] == "class" or tag_list.iat[i, 0] == "class_large":
      printSaliencyColor(i, 'class')
    elif tag_list_custom.iat[i, 0] == "link":
      printSaliencyColor(i, 'link')
    elif tag_list_custom.iat[i, 0] == "span":
      printSaliencyColor(i, 'span')
    elif tag_list_custom.iat[i, 0] == "img":
      printSaliencyColor(i, 'img')
    else:
      printSaliencyColor(i, tag_list_custom.iat[i, 0])

  cv2.imwrite("./output/final.png", halfImg_print ) #Save

  high_element_list_num = len(high_element_list) #配列の長さ取得
  i = 0
  print(high_element_list_num)
  for i in range(high_element_list_num):
    high_element = high_element_list[i]
    start_x = int(tag_list_custom.iat[high_element, 2])
    start_y = int(tag_list_custom.iat[high_element, 3])
    end_x = int(tag_list_custom.iat[high_element, 2]+tag_list_custom.iat[high_element, 4])
    end_y = int(tag_list_custom.iat[high_element, 3]+tag_list_custom.iat[high_element, 5])
    cv2.rectangle(halfImg_print, (start_x, start_y) , (end_x, end_y), (0, 255-(i)*20, 0), 3) #標準： 20ずつ

  # 画像を表示
  cv2.namedWindow("halfImg", cv2.WINDOW_NORMAL)
  cv2.imshow("halfImg", halfImg_print)
  cv2.imwrite("./output/final_importance.png", halfImg_print ) #Save
  k = cv2.waitKey(0)
  if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()


# main
if __name__ == '__main__':
  # 顕著度ランキングの計算
  getHighestSaliency()
  # 最終出力
  getFinalView()
