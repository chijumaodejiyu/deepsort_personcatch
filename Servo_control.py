#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from pca9685 import PCA9685
import datetime


pwm = PCA9685(0x40, debug=True)  # 对象初始化，指定IIC地址
pwm.setPWMFreq(50)  # 设置PWM的频率



class Servo:
    def __init__(self, cel):
        self.nextAngle = None
        self.cel = cel  # 通道设置
        self.deg = 0
        self.time_stamp = datetime.datetime.now()
        self.now_time = None
        print("舵机初始化时间" + str(self.time_stamp))
        pwm.set_servo_angle(cel, 0)  # 重置舵机

    def track(self, track_angle):
        self.now_time = datetime.datetime.now()

        pass

    def run(self, angle):
        self.track(angle)
        time.sleep(0.05)  # 休眠

    def information(self):
        print(self.deg)
        print(self.time_stamp)


test = Servo(0)
if __name__ == '__main__':
    test.information()
