from models.Servo_control import Servo
import numpy as np


class CapTracker:
    def __init__(self, cels: (int, int), screen_shape: (int, int),
                 dxy_p: (float, float) = (0.2, 0.2), dangel: (int, int) = (5, 5)):
        self.cels = cels
        if self.cels[0] != -1:
            self.x_servo = Servo(cels[0])
        else:
            self.x_servo = None
        if self.cels[1] != -1:
            self.servos[1] = Servo(cels[1])
        else:
            self.servos[1] = None
        self.dxy_p = dxy_p
        self.dxy = (dxy_p[0] * screen_shape[0], dxy_p[1] * screen_shape[1])
        self.dangel = dangel
        self.screen_shape = np.array(screen_shape)

    def set_screen_shape(self, screen_shape: (int, int)):
        self.dxy = (self.dxy_p[0] * screen_shape[0], self.dxy_p[1] * screen_shape[1])
        self.screen_shape = screen_shape

    def get_direction(self, item_bbox: list) -> [int, int]:
        x1, y1, x2, y2, _, _ = item_bbox
        direction = [0, 0]
        xc = (x1 + x2 - self.screen_shape[0]) / 2
        yc = (y1 + y2 - self.screen_shape[1]) / 2
        # xc_p = xc / self.screen_shape[0]
        # yc_p = yc / self.screen_shape[1]
        # print(f"Position: {xc_p} : {yc_p}")
        if abs(xc) > self.dxy[0]:
            if xc > 0:
                direction[0] = 1
            else:
                direction[0] = -1
        if abs(yc) > self.dxy[1]:
            if yc > 0:
                direction[1] = 1
            else:
                direction[1] = -1
        return direction

    def track(self, item_bbox: list):
        direction = self.get_direction(item_bbox)
        # print(f"The direction is {direction}.")
        x_direction, y_direction = direction
        if self.x_servo is not None:
            x_angel = self.x_servo.deg + self.dangel[0] * x_direction
            # print(f"The x_angel is {x_angel}.")
            self.x_servo.run(x_angel)
        if self.servos[1] is not None:
            y_angel = self.servos[1].deg + self.dangel[1] * y_direction
            # print(f"The y_angel is {y_angel}.")
            self.servos[1].run(y_angel)


class CapFinder:
    def __init__(self, track_cels: [int, int], screen_shape: [int, int], screen_angel: [int, int],
                 dangel: [int, int] = [10, 10], default_angel: [int, int] = [90, 90]):
        # 初始化数据
        self.track_cels = track_cels
        self.servos = [None, None]
        self.default_angel = default_angel
        self.last_angel = [-1, -1]
        self.dangel = dangel
        self.screen_shape = screen_shape
        self.screen_angel = screen_angel
        # 初始化舵机
        if self.track_cels[0] != -1:
            self.servos[0] = Servo(track_cels[0])
        else:
            self.default_angel[0] = -1
        if self.track_cels[1] != -1:
            self.servos[1] = Servo(track_cels[1])
        else:
            self.default_angel[1] = -1
        self.run(self.default_angel)
    
    def run(self, angel):
        """
        更新舵机角度和角度记录
        Example:
            run((45, 90))  # 一号和二号舵机会分别转至45°和90°
            run((90, -1))  # 一号舵机会转至90°，二号舵机不动
        """
        for i in range(len(angel)):
            if angel[i] != -1:
                self.servos[i].run(angel[i])
                self.last_angel[i] = self.servos[i].deg

    def get_angel(self, item_bbox: list) -> np.ndarray:
        """
        获取相对角度
        """
        # 解压数据
        x1, y1, x2, y2, _, _ = item_bbox
        xy1 = np.array([x1, y1])
        xy2 = np.array([x2, y2])
        screen_angel = np.array(self.screen_angel)
        screen_shape = np.array(self.screen_shape)
        # 计算中心
        xyc = (xy1 + xy2 - screen_shape) / 2
        # 计算角度
        angel = np.arctan(np.tan(screen_angel / 2) * (xyc / self.screen_shape))
        # 转比例
        angel = angel / (np.pi * 2)
        # 转角度制
        angel = 360 * angel
        angel = angel + screen_angel / 2
        print(angel)
        return angel

    def track(self, item_bbox: list):
        """
        追踪相应事物
        """
        # 计算角度
        angel = self.get_angel(item_bbox)
        for i in range(len(self.servos)):
            if self.servos[i] is None:
                angel[i] = -1
        # 计算角度变化值
        dangel = np.abs(self.last_angel - angel)
        # 判断转动要求
        if dangel[0] < self.dangel[0]:
            angel[0] = -1
        if dangel[1] < self.dangel[1]:
            angel[1] = -1
        # 更新角度
        self.run(angel)
