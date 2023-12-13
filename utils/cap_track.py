from Servo_control import Servo
import time
import numpy as np


class CapTracker(Servo):
    def __init__(self, cel, screen_shape: (int, int), screen_deg: int, dangle: int = 5):
        super().__init__(cel)
        self.list_change = time.time()
        self.dangel = dangle
        self.screen_shape = screen_shape
        self.screen_deg = screen_deg

    def get_direction(self, item_bbox: list, screen_shape: (int, int), max_dangel: int) -> [int, int]:
        x1, y1, x2, y2, _, track_id = item_bbox
        direction = [0, 0]
        xc = (x1 + x2 - screen_shape[0]) / 2
        yc = (y1 + y2 - screen_shape[1]) / 2
        if abs(xc) > max_dangel[0]:
            if xc > 0:
                direction[0] = 1
            else:
                direction[0] = -1
        if abs(yc) > max_dangel[0]:
            if yc > 0:
                direction[1] = 1
            else:
                direction[1] = -1
        return direction
