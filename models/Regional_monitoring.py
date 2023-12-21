import numpy as np
import cv2


class Regional_monitoring:
    def __init__(self):
        self.image_dir = "./models/region.png"
        self.monitoring = None
        self.pic_data_read()

    @staticmethod
    def monitoring_process(image: np.ndarray) -> np.ndarray:
        return np.where(image == 0, True, False)

    def pic_data_read(self):
        data = cv2.imread(self.image_dir, cv2.IMREAD_GRAYSCALE)
        if data is None:
            raise ValueError("Failed to load image at {}".format(self.image_dir))
        self.monitoring = self.monitoring_process(data)

    def check(self, item_bbox: list):
        x1, y1, x2, y2, _, _ = item_bbox
        xy1 = np.array([x1, y1])
        xy2 = np.array([x2, y2])
        xyc = (xy1 + xy2) // 2
        out = self.monitoring[xyc[1]][xyc[0]]
        return out

    def draw(self, image):
        picture = image


if __name__ == "__main__":
    test = Regional_monitoring()
    test.check([160, 160, 170, 170, 0, 0])
