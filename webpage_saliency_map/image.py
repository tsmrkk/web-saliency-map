# coding: utf-8
import cv2
import pandas as pd
import numpy as np

class Image:
  def __init__(self, image: cv2):
    self.cv2 = image
    self.height = image.shape[0]
    self.width = image.shape[1]

  def get_halfsize(self) -> cv2:
    size = (int(self.width/2), int(self.height/2))
    image = cv2.resize(self.cv2, size)
    return image

  def get_trimming(self, size: tuple) -> cv2:
    size = (int(size[0]), int(size[1]))
    image = cv2.resize(self.cv2, size)
    return image


class SalientRegionMap:
  def __init__(self, saliency_map: list, screenshot: list, tags: pd, custom_tags: pd):
    self.screenshot = screenshot
    self.saliency_map = saliency_map
    self.canvas = np.zeros((Image(saliency_map).height, Image(saliency_map).width, 3), dtype=np.uint8)
    self.tags = tags
    self.custom_tags = custom_tags
    self.highest_saliency = self.__GetHighestSaliency()

  def GetSortedCustomTagsIndex(self) -> list:
    print(len(self.custom_tags))
    element_area_list = []
    for i in range(len(self.custom_tags) - 1):
      element_area_list.append(int(self.custom_tags.iat[i, 8]))
    return np.argsort(element_area_list)[::-1]

  def GetSalientRegionMap(self):
    for i in self.GetSortedCustomTagsIndex():
      self.__PrintElementBySaliency(i, self.custom_tags.iat[i, 0])
    return self.canvas

  def CreateImportanceMap(self, high_element_list: list):
    high_element_list_num = len(high_element_list) #配列の長さ取得
    i = 0
    print(high_element_list_num)
    for i in range(high_element_list_num):
      high_element = high_element_list[i]
      start_x = int(self.custom_tags.iat[high_element, 2])
      start_y = int(self.custom_tags.iat[high_element, 3])
      end_x = int(self.custom_tags.iat[high_element, 2]+self.custom_tags.iat[high_element, 4])
      end_y = int(self.custom_tags.iat[high_element, 3]+self.custom_tags.iat[high_element, 5])
      cv2.rectangle(self.canvas, (start_x, start_y) , (end_x, end_y), (0, 255-(i)*20, 0), 3) #標準： 20ずつ

    cv2.namedWindow("halfImg", cv2.WINDOW_NORMAL)
    cv2.imshow("halfImg", self.canvas)
    cv2.imwrite("./output/final_importance.png", self.canvas ) #Save
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
      cv2.destroyAllWindows()

  def __GetHighestSaliency(self) -> float:
    return self.custom_tags.iat[self.GetHighSaliencyList()[0], 7]

  def GetHighSaliencyList(self):
    tag_list_num = len(self.custom_tags)
    salient_level = []
    ng_list = []
    high_element_list = []

    # 顕著度を配列に格納
    i = 1 # タイトルの次から実行
    for i in range(tag_list_num):
      if self.custom_tags.iat[i, 0] == "id_large" or self.custom_tags.iat[i, 0] == "class_large":
        salient_level.append(-1)
      else:
        salient_level.append(self.custom_tags.iat[i, 7])

    salient_level_sort_final = np.argsort(salient_level)

    salient_num = 10 # 上位何個表示するか？
    temporal_num = 1 # 一時的な変数
    salient_num_first = salient_num

    while salient_num > 0 :
      most_salient = salient_level_sort_final[tag_list_num - temporal_num]
      print(most_salient)
      if (most_salient in ng_list) == False:
        start_x = int(self.custom_tags.iat[most_salient, 2])
        start_y = int(self.custom_tags.iat[most_salient, 3])
        end_x = int(self.custom_tags.iat[most_salient, 2]+self.custom_tags.iat[most_salient, 4])
        end_y = int(self.custom_tags.iat[most_salient, 3]+self.custom_tags.iat[most_salient, 5])
        size = int(self.custom_tags.iat[most_salient, 4]*self.custom_tags.iat[most_salient, 5])
        if start_x < 0 :
          start_x = 0
        if start_y < 0 :
          start_y = 0
        if end_x > Image(self.saliency_map).width:
          end_x = Image(self.saliency_map).width
        if end_y > Image(self.saliency_map).height:
          end_y = Image(self.saliency_map).height

        if (end_x - start_x)/(end_y - start_y) < 10: # あまりにも細長いものを排除
          clipped = self.screenshot[int(start_y):int(end_y),int(start_x):int(end_x)]
          cv2.imwrite("./working/high-saliency/img"+ str(salient_num_first - salient_num + 1) +".png", clipped ) #Save
          print("画像出力 & 顕著度高いリストに追加")
          high_element_list.append(most_salient)
          salient_num -= 1

          print("%s %s %s %s 顕著度→%s" %(start_x, start_y, end_x, end_y, self.custom_tags.iat[most_salient, 7]) )

          i = 1 # タイトルの次から実行
          for i in range(tag_list_num):
            if (i in ng_list) == False:
              research_start_x = int(self.custom_tags.iat[i, 2])
              research_start_y = int(self.custom_tags.iat[i, 3])
              research_end_x = int(self.custom_tags.iat[i, 2]+self.custom_tags.iat[i, 4])
              research_end_y = int(self.custom_tags.iat[i, 3]+self.custom_tags.iat[i, 5])
              research_size = int(self.custom_tags.iat[most_salient, 4]*self.custom_tags.iat[most_salient, 5])

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

    return high_element_list

  # 各要素の塗り潰し関数
  def __PrintElementBySaliency(self, i: int, type: str):
    start_x = int(self.custom_tags.iat[i, 2])
    start_y = int(self.custom_tags.iat[i, 3])
    end_x = int(self.custom_tags.iat[i, 2]+self.custom_tags.iat[i, 4])
    end_y = int(self.custom_tags.iat[i, 3]+self.custom_tags.iat[i, 5])
    # 最も顕著度の高い要素を最大輝度で塗りつぶす
    salient_level_num = (self.custom_tags.iat[i, 7] / self.highest_saliency) * 256
    if salient_level_num > 0:
      cv2.rectangle(self.canvas, (start_x, start_y) , (end_x, end_y), (salient_level_num, salient_level_num, salient_level_num), -1)

    # ToDo 現在画像のみそのまま表示するシステムは使用していない
    # if type == 'img' and ((end_x - start_x)*(end_y - start_y)) / (Image(self.saliency_map).width * Image(self.saliency_map).height) > 0.1 :
    #   if start_x < 0 or start_y < 0 or end_x > Image(self.saliency_map).width or end_y > Image(self.saliency_map).height:
    #     return

    #   clipped = self.screenshot[start_y:end_y,start_x:end_x]
    #   print(clipped.shape)
    #   print(start_x, start_y)
    #   self.canvas[start_y:clipped.shape[0] + start_y, start_x:clipped.shape[1] + start_x] = clipped
    # else :
    #   if salient_level_num > 0:
    #     cv2.rectangle(self.canvas, (start_x, start_y) , (end_x, end_y), (salient_level_num, salient_level_num, salient_level_num), -1)

