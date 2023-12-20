import numpy as np
import cv2


class Regional_monitoring:
    def __init__(self):
        self.image_dir = "../models/region.png"
        self.monitoring = None
        self.pic_data_read()

    def monitoring_process(self, image: np.ndarray) -> np.ndarray:
        return np.where(image == 0, True, False)

    def pic_data_read(self):
        data = cv2.imread(self.image_dir, cv2.IMREAD_GRAYSCALE)
        self.monitoring = self.monitoring_process(data)
        return data

    def check(self, item_bbox: list):
        x1, y1, x2, y2, _, _ = item_bbox
        xy1 = np.array([x1, y1])
        xy2 = np.array([x2, y2])
        xyc = (xy1 + xy2) // 2
        out = self.monitoring[xyc[1]][xyc[0]]
        return out


if __name__ == "__main__":
    test = Regional_monitoring()
    test.check([160, 160, 170, 170, 0, 0])
