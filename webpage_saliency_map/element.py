# coding: utf-8
import cv2
import math
import numpy as np

from image import Image

class Element:
  canvas = ''

  def __init__(self, data: list, type: str):
    self.type = type
    if type == 'id':
      self.tag_name = data.get_attribute('id')
    elif type == "class":
      self.tag_name = data.get_attribute('class')
    elif type == "img":
      self.tag_name = 'image'
    else:
      self.tag_name = type
    self.start_x = data.location['x']
    self.start_y = data.location['y']
    self.width = data.size['width']
    self.height = data.size['height']
    self.end_x = self.start_x + self.width
    self.end_y = self.start_y + self.height
    # displayed area
    self.d_start_x = 0 if self.start_x < 0 else (Element.canvas.width if self.start_x > Element.canvas.width else self.start_x)
    self.d_start_y = 0 if self.start_y < 0 else (Element.canvas.width if self.start_y > Element.canvas.height else self.start_y)
    self.d_end_x = Element.canvas.width if self.end_x > Element.canvas.width else (0 if self.end_x < 0 else self.end_x)
    self.d_end_y = Element.canvas.height if self.end_y > Element.canvas.height else (0 if self.end_y < 0 else self.end_y)
    self.d_width = self.d_end_x - self.d_start_x
    self.d_height = self.d_end_y - self.d_start_y
    self.d_area = self.d_width * self.d_height
    print(self.tag_name)
    print(self.d_start_x, self.d_start_y, self.d_end_x, self.d_end_y, self.d_width, self.d_height, self.d_area)

  @staticmethod
  def GetTotalSaliency():
    # ToDo なんか出力がおかしいから計算する
    clipped = Element.canvas.cv2[0:int(Element.canvas.height), 0:int(Element.canvas.width)]
    total_saliency_per_row = np.sum(clipped, axis=0)
    total_saliency = np.sum(total_saliency_per_row, axis=0)
    return total_saliency
    

  def GetAverageColor(self) -> float:
    if self.start_x < 0:
      self.start_x = 0
    if self.start_y < 0:
      self.start_y = 0
    if self.start_x < Element.canvas.width and self.start_y < Element.canvas.height and self.width > 0 and self.height > 0:
      if self.end_x > Element.canvas.width:
          end_x = int(Element.canvas.width)
      if self.end_y > Element.canvas.height:
          end_y = int(Element.canvas.height)
      clipped = Element.canvas.cv2[int(self.start_y):int(self.end_y), int(self.start_x):int(self.end_x)]
      average_color_per_row = np.average(clipped, axis=0)
      average_color = np.average(average_color_per_row, axis=0)
      average_color = np.uint8(average_color)
      return average_color
    else:
      return 0
  
  # 要素の顕著度の合計を取得
  def GetTotalSalientLevel(self) -> float:
    if self.start_x < 0:
      self.start_x = 0
    if self.start_y < 0:
      self.start_y = 0
    if self.start_x < Element.canvas.width and self.start_y < Element.canvas.height and self.width > 0 and self.height > 0:
      if self.end_x > Element.canvas.width:
          end_x = int(Element.canvas.width)
      if self.end_y > Element.canvas.height:
          end_y = int(Element.canvas.height)
      # print(int(self.start_x), int(self.start_y), int(self.end_x), int(self.end_y))
      clipped = Element.canvas.cv2[int(self.start_y):int(self.end_y), int(self.start_x):int(self.end_x)]
      total_saliency_per_row = np.sum(clipped, axis=0)
      total_saliency = np.sum(total_saliency_per_row, axis=0)
      return total_saliency
    else:
      return 0


  # 要素の顕著度を計算する関数（新バージョン）
  def GetSalientLevelNum(self, average_color) -> float:
    # ToDo: 重み付けをタイプごとに変更する方式を採用 

    digit = 4
    digit10 = 10 ** (digit - 1)
    print('Total saliency: ' + str(self.GetTotalSalientLevel()))
    if self.d_area != 0:
      salient_level = self.GetTotalSalientLevel() / (Element.GetTotalSaliency() * (self.d_area / (Element.canvas.width * Element.canvas.height)))
    else:
      salient_level = 0
    print('Salient Level: ' + str(salient_level))
    return math.floor(salient_level * digit10) / digit10
  
  # 要素の顕著度を計算する関数（旧バージョン）
  def GetSalientLevelNumOld(self, average_color) -> float:
    salient_level_weight = (self.end_x - self.start_x) * (self.end_y - self.start_y)
    if salient_level_weight > 1000:
      salient_level_num = average_color
    elif salient_level_weight > 800:
      salient_level_num = average_color*0.7
    elif salient_level_weight > 500:
      salient_level_num = average_color*0.6
    else:
      salient_level_num = average_color*0.2
    
    place_weight_x = 0.1  # 最低圧縮値(0~1) 0.1
    place_weight_y = 0.4  # 最低圧縮値(0~1) 0.3
    center_weight = 0.2  # 最低圧縮値(0~1) 0.3

    if self.width < int(Element.canvas.width) and self.height < int(Element.canvas.height):
      topleft_bias = (1 - (place_weight_y - ((int(Element.canvas.height) - (self.start_y + self.height/2)) * place_weight_y / int(Element.canvas.height)))) * (1 - (place_weight_x - ((int(Element.canvas.width) - (self.start_x + self.width/2)) * place_weight_x / int(Element.canvas.width))))

      center_bias_x = abs(int(Element.canvas.width)/2 - (self.start_x + self.width/2)) * \
                abs(int(Element.canvas.width)/2 - (self.start_x + int(Element.canvas.width)/2))
      center_bias_y = abs(int(Element.canvas.height)/2 - (self.start_y + self.height/2)) * \
                abs(int(Element.canvas.height)/2 - (self.start_y + self.height/2))
      center_bias_calc = np.sqrt(center_bias_x + center_bias_y) / np.sqrt(int(Element.canvas.width) * int(Element.canvas.width) + int(Element.canvas.height) * int(Element.canvas.height))

      salient_level_num = salient_level_num * (topleft_bias - (center_weight * center_bias_calc))
      return salient_level_num
    else:
      return 0
  
  def WriteDataToCsv(self, csv_writer, csv_tags_custom):
    average_color = self.GetAverageColor()
    salient_level_num = self.GetSalientLevelNum(average_color)
    if (self.width * self.height) > (Element.canvas.width * 800 / 3):
      csv_writer.writerow([self.type + '_large', self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num, self.d_area])
    else:
      csv_writer.writerow([self.type, self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num, self.d_area])
    
    if salient_level_num > 0:
      csv_tags_custom.writerow([self.type, self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num, self.d_area])
    