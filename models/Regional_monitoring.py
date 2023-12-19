import numpy as np
import cv2


class Regional_monitoring:
    def __init__(self):
        # self.region = region_input
        self.solid_coordinates = None
        self.track_id = -1
        self.image_dir = r"./models/region.png"

    def pic_data_read(self):
        data = cv2.imread(self.image_dir)
        print(data)

    def check(self, item_bbox: list):
        try:
            x1, y1, x2, y2, _, _ = item_bbox
            xy1 = np.array([x1, y1])
            xy2 = np.array([x2, y2])
            xyc = (xy1 + xy2) / 2
            print(xyc)
            # self.solid_coordinates = np.mat(((self.x1 + self.x2) / 2), ((self.y1 + self.y2) / 2))

        except:
            print('can not read item_bbox successfully')
            pass


if __name__ == "__main__":
    test = Regional_monitoring()
    test.pic_data_read()
