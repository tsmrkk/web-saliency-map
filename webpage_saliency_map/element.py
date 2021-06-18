# coding: utf-8
import cv2
import math
import numpy as np

from image import Image

class Element:
  canvas = ''
  layout_type = 1
  model = ''

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
    self.d_center = ((self.d_start_x + self.width/2), (self.start_y + self.height/2))
    self.selector = "hello"
    print('[' + self.type + ']' + ' ' +self.tag_name)
    print(self.d_start_x, self.d_start_y, self.d_end_x, self.d_end_y, self.d_width, self.d_height, self.d_area)

  def WriteCSV(self, writer, typeName, average_color, salient_level_num):
    writer.writerow([typeName, self.tag_name, self.start_x, self.start_y, self.width, self.height, average_color, salient_level_num, self.d_area, self.selector])

  @staticmethod
  def GetTotalSaliency():
    clipped = Element.canvas.cv2[0:int(Element.canvas.height), 0:int(Element.canvas.width)]
    total_saliency_per_row = np.sum(clipped, axis=0)
    total_saliency = np.sum(total_saliency_per_row, axis=0)
    return total_saliency

  # 要素データCSV書き込み関数
  def WriteDataToCsv(self, csv_writer, csv_tags_custom):
    average_color = self.__GetAverageColor()
    salient_level_num = self.GetSalientLevelNum(average_color)
    if (self.width * self.height) > (Element.canvas.width * 800 / 3):
      self.WriteCSV(csv_writer, self.type + '_large', average_color, salient_level_num)
    else:
      self.WriteCSV(csv_writer, self.type, average_color, salient_level_num)
    if salient_level_num > 0:
      self.WriteCSV(csv_tags_custom, self.type, average_color, salient_level_num)

  # 要素の顕著度を計算する関数（新バージョン）
  def GetSalientLevelNum(self, average_color) -> float:
    digit = 4 # 小数点第４位まで
    digit10 = 10 ** (digit - 1)
    if self.d_area != 0:
      salient_level = self.__GetTotalSalientLevel() / (Element.GetTotalSaliency() * (self.d_area / (Element.canvas.width * Element.canvas.height)))
      if Element.model not in ['original', 'original-mlnet']:
        salient_level = self.__ApplyPositionBias(salient_level)
        salient_level = self.__ApplySizeBias(salient_level)
    else:
      salient_level = 0

    print('Element area: ' + str(self.d_area))
    print('Total saliency: ' + str(self.__GetTotalSalientLevel()))
    print('Salient Level: ' + str(salient_level))
    return math.floor(salient_level * digit10) / digit10

  # 位置情報に関するバイアスを適応
  def __ApplyPositionBias(self, salient_level: float) -> float:
    highsaliency = False
    bias_info_list = [
      [
        ((556.535, 368.237), 444.828, 237.783),
        ((680.655, 438.258), 466.895, 308.361),
        ((707.529, 496.782), 349.648, 278.916),
        ((768.129, 511.911), 408.867, 338.986),
        ((788.448, 515.606), 389.028, 352.117)
      ],
      [
        ((537.908, 327.895), 371.117, 84.034),
        ((638.071, 436.232), 396.092, 131.802),
        ((673.810, 500.411), 382.184, 202.550),
        ((748.266, 563.434), 338.235, 204.414),
        ((738.184, 583.134), 359.403, 226.293)
      ],
      [
        ((553.667, 375.013), 156.000, 74.330),
        ((630.304, 442.511), 197.017, 190.908),
        ((740.487, 524.988), 250.856, 172.198),
        ((692.258, 558.338), 371.499, 154.666),
        ((729.131, 544.055), 271.238, 152.742)
      ],
      [
        ((622.936, 403.412), 39.819, 23.291),
        ((652.957, 587.204), 57.615, 43.529),
        ((550.208, 680.730), 119.848, 132.474),
        ((741.046, 624.545), 129.733, 175.200),
        ((926.995, 530.668), 172.676, 87.606)
      ],
      [
        ((569.893, 310.072), 248.882, 51.797),
        ((612.145, 391.966), 399.641, 78.470),
        ((688.601, 481.164), 166.225, 119.729),
        ((723.868, 507.663), 216.520, 128.412),
        ((782.715, 540.818), 194.260, 152.851)
      ],
      [
        ((645.740, 458.442), 466.027, 326.286),
        ((682.060, 494.166), 596.618, 335.889),
        ((740.436, 500.645), 522.822, 322.047),
        ((783.374, 520.623), 530.180, 292.100),
        ((759.123, 529.811), 360.045, 305.448)
      ],
      [
        ((640.267, 423.961), 298.253, 184.015),
        ((673.685, 472.424), 359.912, 197.110),
        ((672.597, 542.487), 497.066, 264.812),
        ((694.481, 545.091), 389.884, 221.839),
        ((722.543, 520.624), 484.229, 333.351)
      ]
    ]
    for bias_info in bias_info_list[int(Element.layout_type)-1]:
      if self.__JudgeInsideEllipse(self.d_center, bias_info):
        highsaliency = True

    if highsaliency:
      return salient_level * 2
    else:
      return salient_level

  # サイズに関するバイアスを適応
  def __ApplySizeBias(self, salient_level: float) -> float:
    if self.d_area < 500:
      return salient_level / 2
    else:
      return salient_level

  # 楕円の内側かどうかを判断する関数
  def __JudgeInsideEllipse(self, judge_coordinate: tuple, bias_info: tuple) -> bool:
    center_coordinate = bias_info[0]
    x_radius = bias_info[1]
    y_radius = bias_info[2]
    magnification_axis = 'x' # 補正座標
    magnification_value = 0 # 補正値
    if x_radius > y_radius:
      magnification_axis = 'y'
      magnification_value = x_radius / y_radius
    else:
      magnification_axis = 'x'
      magnification_value = y_radius / x_radius

    if magnification_axis == 'y':
      x = center_coordinate[0] - judge_coordinate[0]
      y = magnification_value * ( center_coordinate[1] - judge_coordinate[1] )
      if math.sqrt(x**2 + y**2) <= x_radius:
        return True
      else:
        return False
    else:
      x = magnification_value * ( center_coordinate[0] - judge_coordinate[0] )
      y = center_coordinate[1] - judge_coordinate[1]
      if math.sqrt(x**2 + y**2) <= y_radius:
        return True
      else:
        return False


  # 要素の顕著度の平均を取得
  def __GetAverageColor(self) -> float:
    if self.d_width > 0 and self.d_height > 0:
      clipped = Element.canvas.cv2[int(self.d_start_y):int(self.d_end_y), int(self.d_start_x):int(self.d_end_x)]
      average_color_per_row = np.average(clipped, axis=0)
      average_color = np.average(average_color_per_row, axis=0)
      average_color = np.uint8(average_color)
      return average_color
    else:
      return 0

  # 要素の顕著度の合計を取得
  def __GetTotalSalientLevel(self) -> float:
    if self.d_width > 0 and self.d_height > 0:
      clipped = Element.canvas.cv2[int(self.d_start_y):int(self.d_end_y), int(self.d_start_x):int(self.d_end_x)]
      total_saliency_per_row = np.sum(clipped, axis=0)
      total_saliency = np.sum(total_saliency_per_row, axis=0)
      return total_saliency
    else:
      return 0
