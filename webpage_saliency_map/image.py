# coding: utf-8
import cv2

class Image:
  def __init__(self, image: cv2):
    self.cv2 = image
    self.height = image.shape[0]
    self.width = image.shape[1]

  def get_halfsize(self) -> cv2:
    size = (int(self.width/2), int(self.height/2))
    image = cv2.resize(self.cv2, size)
    return image
