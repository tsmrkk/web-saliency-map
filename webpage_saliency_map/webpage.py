# coding: utf-8
import cv2
import numpy as np
import pySaliencyMap
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup

class Webpage:
  def __init__(self, url):
    self.url = url
    binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox')
    binary.add_command_line_options('-headless')
    self.driver = webdriver.Firefox(firefox_binary=binary)

  def get_screenshot(self, file_name: str, window_width: int, window_height: int) -> cv2:
    self.driver.get(self.url)
    print('Get screenshot...')
    self.driver.set_window_size(window_width, window_height)
    soup = BeautifulSoup(self.driver.page_source, "html.parser")
    self.soup = soup

    page_height = self.driver.execute_script('return document.body.scrollHeight')
    scrollHeight = self.driver.execute_script('return window.innerHeight')

    print(scrollHeight)

    input("アニメーション等の読み込みが完了したらEnterを押してください\n")
    self.driver.save_screenshot('./working/' + file_name)
    return cv2.imread('./working/' + file_name)

  def get_saliency_map(self, image: cv2) -> cv2:
    imgsize = image.shape
    img_width = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    # computation
    print("Calculating Saliency map...")
    saliency_map = sm.SMGetSM(image)
    print("Calculating Binarized map...")
    binarized_map = sm.SMGetBinarizedSM(image)
    # グレースケール（２値化）に変換
    print("Convert to gray scale saliency map...")
    saliency_map = saliency_map.astype(np.float64)
    saliency_map = saliency_map * 255
    saliency_map = saliency_map.astype(np.uint8)
    print("Output Complete")
    cv2.imwrite("./output/saliency_map.png", saliency_map)
    return saliency_map

  def save_html(self):
    print("Load and save HTML...")
    output_html = self.soup.prettify()
    f = open('./output/index.html', 'w')
    f.write(output_html)
    f.close()
