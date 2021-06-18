# coding: utf-8
import cv2
import sys

from webpage import Webpage
from file import Csv
from element import Element
from image import Image
from finalline import getFinalLine
from finalview2 import CreateRegionMap
from finaltile import getFinalTile

def SetElementInfo(queryName, query, webpage, csv_tags, csv_tags_custom):
  # print(f"Getting position and size of {query}")
  els = webpage.driver.find_elements_by_xpath(query)
  for el in els:
    if str(el.is_displayed()) == "True":  # 表示されている時のみリストに挿入
      element = Element(el, queryName)
      element.SetSelector(el)
      element.WriteDataToCsv(csv_tags, csv_tags_custom)

# get element information
def GetElementInfo(webpage, csv_tags, csv_tags_custom):
  queryDict = {
      "id": "//div[@id]",
      "class": '//div[@class]',
      "h1": '//h1',
      "h2": '//h2',
      "h3": '//h3',
      "link": '//a',
      "span": '//span',
      "p": '//p',
      "img": '//img'
  }
  for k, v in queryDict.items():
    SetElementInfo(k, v, webpage, csv_tags, csv_tags_custom)

# main function
def main(models = None):
  models = [] if models is None else models.split(',')
  models.insert(0, 'original')
  print("Generate results -> " + str(models))
  url = input("URLを入力してください\n")
  layout_type = input("タイプを選択してください(1-7)\n")
  webpage = Webpage(url, layout_type)

  # スクリーンショット取得
  screenshot = webpage.get_screenshot('screen-pc.png', 1280, 800)
  # HTML保存
  webpage.save_html()

  for model in models:
    print(model)
    # CSVの準備
    csv_tags = Csv('./working/tag_list_' + model + '.csv')
    csv_tags_custom = Csv('./working/tag_list_custom_' + model + '.csv')
    default_row = [
      'class or id',
      'tag_name',
      'start_x',
      'start_y',
      'size_w',
      'size_h',
      'average_color',
      'salient_level',
      'element_area',
      'selector'
    ]
    csv_tags.writerow(default_row)
    csv_tags_custom.writerow(default_row)

    # ハーフサイズの顕著性マップ
    if model == 'original':
      # 顕著性マップ取得
      saliency_map = webpage.get_saliency_map(screenshot)
      resize_saliency_map = Image(saliency_map).get_halfsize()
    elif model == 'original-mlnet':
      saliency_map = Image(cv2.imread('./data/mlnet.png', 1))
      resize_saliency_map = saliency_map.get_trimming((1280, 726))
      resize_saliency_map = cv2.cvtColor(resize_saliency_map, cv2.COLOR_BGR2GRAY)
    else:
      saliency_map = Image(cv2.imread('./data/' + model + '.png', 1))
      resize_saliency_map = saliency_map.get_trimming((1280, 726))
      resize_saliency_map = cv2.cvtColor(resize_saliency_map, cv2.COLOR_BGR2GRAY)

    # 各要素のサイズと顕著度を取得
    Element.canvas = Image(resize_saliency_map)
    Element.layout_type = webpage.layout_type
    Element.model = model
    # print('ウェブページ全体の顕著度：' + str(Element.GetTotalSaliency()))

    GetElementInfo(webpage, csv_tags, csv_tags_custom)

    # CSVとWebDriverのClose
    csv_tags.close()
    csv_tags_custom.close()
    CreateRegionMap(model)

  webpage.driver.quit()
  getFinalLine()
  getFinalTile()

if __name__ == '__main__':
  if sys.argv[1:2]:
    main(sys.argv[1])
  else:
    main()
