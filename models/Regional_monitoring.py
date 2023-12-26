import numpy as np
import cv2
import os


class Regional_monitoring:
    def __init__(self):
        # 定义监控图像路径
        self.image_dir = "region.png"
        # 初始化监控数据，稍后在读取图像后赋值
        self.monitoring = None
        # 读取图像数据
        self.pic_data_read()

    @staticmethod
    def monitoring_process(image: np.ndarray) -> np.ndarray:
        # 将图像中所有像素值为0的位置标记为True，其余位置为False
        return np.where(image == 0, True, False)

    def pic_data_read(self):
        # 检测图像文件是否被丢进了次元空间
        print(os.path.exists(self.image_dir))
        # 使用OpenCV读取图像，并转换为灰度模式
        data = cv2.imread(self.image_dir, cv2.IMREAD_GRAYSCALE)
        # 检查图像是否正确加载
        if data is None:
            raise ValueError("Failed to load image at {}".format(self.image_dir))
            # 处理图像数据，得到监控区域的布尔数组
        self.monitoring = self.monitoring_process(data)

    def check(self, item_bbox: list):
        # 从传入的边界框列表中解包出坐标信息
        x1, y1, x2, y2, _, _ = item_bbox
        # 创建左上角和右下角的坐标点
        xy1 = np.array([x1, y1])
        xy2 = np.array([x2, y2])
        # 计算边界框的中心点坐标（注意这里是整数除法）
        xyc = (xy1 + xy2) // 2
        # 使用中心点坐标检查监控区域的布尔值
        out = self.monitoring[xyc[1]][xyc[0]]
        return out

    def draw(self, im):
        alpha = 0.2
        beta = 1 - alpha
        picture1 = cv2.imread(self.image_dir)
        picture2 = im
        img_alpha = cv2.addWeighted(picture1, alpha, picture2, beta, 0)  # 图像融合
        return img_alpha


if __name__ == "__main__":
    # 创建Regional_monitoring类的实例
    test = Regional_monitoring()
    # 检查给定边界框[160, 160, 170, 170, 0, 0]是否在监控区域内
    test.check([160, 160, 170, 170, 0, 0])
    im = cv2.imread('2023-12-19_17-22-12-141.jpg')
    cv2.imshow("危险区域叠加图层展示", test.draw(im))
    cv2.waitKey(0)
