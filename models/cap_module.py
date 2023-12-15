from Servo_control import Servo
import time
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
            self.y_servo = Servo(cels[1])
        else:
            self.y_servo = None
        self.dxy_p = dxy_p
        self.dxy = (dxy_p[0] * screen_shape[0], dxy_p[1] * screen_shape[1])
        self.dangel = dangel
        self.screen_shape = screen_shape

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
        if self.y_servo is not None:
            y_angel = self.y_servo.deg + self.dangel[1] * y_direction
            # print(f"The y_angel is {y_angel}.")
            self.y_servo.run(y_angel)


class CapFinder:
    def __init__(self, cels: (int, int), screen_shape: (int, int),
                 dxy_p: (float, float) = (0.2, 0.2), dangel: (int, int) = (30, 30)):
        self.cels = cels
        if self.cels[0] != -1:
            self.x_servo = Servo(cels[0])
        else:
            self.x_servo = None
        if self.cels[1] != -1:
            self.y_servo = Servo(cels[1])
        else:
            self.y_servo = None
        self.dxy_p = dxy_p
        self.dxy = (dxy_p[0] * screen_shape[0], dxy_p[1] * screen_shape[1])
        self.dangel = dangel
        self.screen_shape = screen_shape

    def set_screen_shape(self, screen_shape: (int, int)):
        self.dxy = (self.dxy_p[0] * screen_shape[0], self.dxy_p[1] * screen_shape[1])
        self.screen_shape = screen_shape

    def get_direction(self, item_bbox: list) -> [int, int]:
        x1, y1, x2, y2, _, _ = item_bbox
        direction = [0, 0]
        xc = (x1 + x2 - self.screen_shape[0]) / 2
        yc = (y1 + y2 - self.screen_shape[1]) / 2
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
        pass

    def get_tracker_position(self, tracker_image: np.ndarray):
        pass