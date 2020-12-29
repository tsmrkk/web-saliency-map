# coding: utf-8
from webpage import Webpage
from file import Csv
from element import Element
from image import Image
from finalline import getFinalLine
from finalview import getHighestSaliency, getFinalView
from finalview2 import CreateRegionMap
from finaltile import getFinalTile

# main function
def main():
  url = input("URLを入力してください\n")
  webpage = Webpage(url)

  # スクリーンショット取得
  screenshot = webpage.get_screenshot('screen-pc.png', 1280, 800)
  # 顕著性マップ取得
  saliency_map = webpage.get_saliency_map(screenshot)
  # HTML保存
  webpage.save_html()

  # CSVの準備
  csv_tags = Csv('./working/tag_list.csv')
  csv_tags_custom = Csv('./working/tag_list_custom.csv')
  default_row = [
    'class or id',
    'tag_name',
    'start_x',
    'start_y',
    'size_w',
    'size_h',
    'average_color',
    'salient_level',
    'element_area'
  ]
  csv_tags.writerow(default_row)
  csv_tags_custom.writerow(default_row)

  # ハーフサイズの顕著性マップ
  resize_saliency_map = Image(saliency_map).get_halfsize()

  # 各要素のサイズと顕著度を取得
  Element.canvas = Image(resize_saliency_map)
  print('ウェブページ全体の顕著度：' + str(Element.GetTotalSaliency()))

  print("Getting position and size of //div[@id]")
  tags_id = webpage.driver.find_elements_by_xpath("//div[@id]")
  for tag_id in tags_id:
    if str(tag_id.is_displayed()) == "True":  # 表示されている時のみリストに挿入
      element = Element(tag_id, 'id')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)
      print('要素の顕著度：' + str(element.GetTotalSalientLevel()))

  print("Getting position and size of //div[@class]")
  tags_class = webpage.driver.find_elements_by_xpath('//div[@class]')
  for tag_class in tags_class:
    if str(tag_class.is_displayed()) == "True":  # 表示されている時のみリストに挿入
      element = Element(tag_class, 'class')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)
      print('要素の顕著度：' + str(element.GetTotalSalientLevel()))

  print("Getting position and size of //h1")
  elements = webpage.driver.find_elements_by_xpath('//h1')
  for element in elements:
    if str(element.is_displayed()) == "True":
      element = Element(element, 'h1')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)

  print("Getting position and size of //h2")
  elements = webpage.driver.find_elements_by_xpath('//h2')
  for element in elements:
    if str(element.is_displayed()) == "True":
      element = Element(element, 'h2')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)

  print("Getting position and size of //h3")
  elements = webpage.driver.find_elements_by_xpath('//h3')
  for element in elements:
    if str(element.is_displayed()) == "True":
      element = Element(element, 'h3')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)

  print("Getting position and size of //a")
  elements = webpage.driver.find_elements_by_xpath('//a')
  for element in elements:
    if str(element.is_displayed()) == "True":
      element = Element(element, 'link')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)

  print("Getting position and size of //span")
  elements = webpage.driver.find_elements_by_xpath('//span')
  for element in elements:
    if str(element.is_displayed()) == "True":
      element = Element(element, 'span')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)
  
  print("Getting position and size of //div[@image]")
  elements = webpage.driver.find_elements_by_xpath('//img')
  for element in elements:
    if str(element.is_displayed()) == "True":
      element = Element(element, 'img')
      element.WriteDataToCsv(csv_tags, csv_tags_custom)

  # CSVとWebDriverのClose
  csv_tags.close()
  csv_tags_custom.close()
  webpage.driver.quit()

  getFinalLine()
  # getHighestSaliency()
  # getFinalView()
  CreateRegionMap()
  getFinalTile()

if __name__ == '__main__':
  main()
