import cv2
import numpy as np

def getFinalTile():
  im1 = cv2.imread('./working/high-saliency/img1.png')
  im2 = cv2.imread('./working/high-saliency/img2.png')
  im3 = cv2.imread('./working/high-saliency/img3.png')
  im4 = cv2.imread('./working/high-saliency/img4.png')
  im5 = cv2.imread('./working/high-saliency/img5.png')
  im6 = cv2.imread('./working/high-saliency/img6.png')
  im7 = cv2.imread('./working/high-saliency/img7.png')
  im8 = cv2.imread('./working/high-saliency/img8.png')
  im9 = cv2.imread('./working/high-saliency/img9.png')
  im10 = cv2.imread('./working/high-saliency/img10.png')

  def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)

  def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_max = max(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_max, int(im.shape[0] * w_max / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

  def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_max = max(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_max / im.shape[0]), h_max), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

  im_tile_resize = concat_tile_resize([[im1, im2], [im3, im4, im5], [im6, im7, im8, im9, im10]])
  cv2.imwrite('./output/final_tile.png', im_tile_resize)

# main
if __name__ == '__main__':
  getFinalTile()
