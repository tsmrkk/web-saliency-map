# coding: utf-8
import cv2
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
    print(self.tag_name)

  def get_average_color(self) -> float:
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

  def get_salient_level_num(self, average_color) -> float:
    # 重み付け箇所 サイズによる重み付け
    salient_level_weight = (self.end_x - self.start_x) * (self.end_y - self.start_y)
    if salient_level_weight > 1000:
      salient_level_num = average_color
    elif salient_level_weight > 800:
      salient_level_num = average_color*0.7
    elif salient_level_weight > 500:
      salient_level_num = average_color*0.6
    else:
      salient_level_num = average_color*0.2
    
    # 位置による重み付け
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
  
  def write_data_to_csv(self, csv_writer, csv_tags_custom):
    average_color = self.get_average_color()
    salient_level_num = self.get_salient_level_num(average_color)
    if (self.width * self.height) > (Element.canvas.width * 800 / 3):
      csv_writer.writerow([self.type + 'large', self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num])
    else:
      csv_writer.writerow([self.type, self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num])
    
    if salient_level_num > 0:
      csv_tags_custom.writerow([self.type, self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num])

      
