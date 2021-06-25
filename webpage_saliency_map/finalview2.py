# coding: utf-8
import cv2
import pandas as pd

from image import Image, SalientRegionMap

# main function
def CreateRegionMap(model, fileName):
  row_saliencymap = cv2.imread("./output/saliency_map.png", 1)
  row_screenshot = cv2.imread("./working/screen-pc.png", 1)

  saliencymap = Image(row_saliencymap).get_halfsize()
  screenshot = Image(row_screenshot).get_halfsize()
  tag_list = pd.read_csv('./working/tag_list_' + model + '.csv')
  tag_list_custom = pd.read_csv('./working/tag_list_custom_' + model + '.csv')
  salient_region_map = SalientRegionMap(saliencymap, screenshot, tag_list, tag_list_custom)

  # Salient Region Map の生成
  cv2.imwrite('./output/' + model + '.png', salient_region_map.GetSalientRegionMap() )

  # 重要領域マップの生成
  if model == 'original':
    high_element_list = salient_region_map.GetHighSaliencyList()
    salient_region_map.CreateSaliencyCSVRanking(high_element_list, fileName)
    salient_region_map.CreateImportanceMap(high_element_list)

if __name__ == '__main__':
  CreateRegionMap()
