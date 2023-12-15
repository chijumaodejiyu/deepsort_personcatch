import cv2
import numpy as np


def matching_img(image: np.ndarray, part_image: np.ndarray,
                 difference: float = 1.0, step: float = 0.7, min_shape: (int, int) = (10, 10)) -> (int, int, int, int):
    # 数据定义
    part_shape = part_image.shape
    difference_map = []

    while part_shape[0] > min_shape[0] and part_shape[1] > min_shape[1]:
        pass


def get_difference(image1: np.ndarray, image2: np.ndarray) -> float:
    # 形状判断
    if image1.shape != image2.shape:
        print("The shapes of the two images is not same.")
        return -1
    # 颜色转换 BGR -> GRAY
    im1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # 差值
    dimage = (im1 - im2).astype(np.int16)
    # 最小值
    min_val = np.min(dimage)
    dimage = dimage - min_val
    # 所有差值
    all_difference = np.sum(dimage)
    difference = all_difference / (im1.shape[0] * im1.shape[1])

    return difference
