#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from pca9685 import PCA9685
import random

pwm = PCA9685(0x40, debug=True)  # 对象初始化，指定IIC地址
pwm.setPWMFreq(50)  # 设置PWM的频率


class Servo:
    def __init__(self, cel):
        self.nextAngle = None
        self.cel = cel  # 通道设置
        self.deg = 0  # 舵机角度记忆
        self.time_stamp = round(time.time(), 3)  # 时间戳
        print('时间戳'+str(self.time_stamp))
        self.now_time = None
        print("舵机初始化时间" + str(self.time_stamp))
        pwm.set_servo_angle(cel, 0)  # 重置舵机

    def track(self, track_angle):
        self.now_time = round(time.time(), 3)
        print('计算出的时间差'+str(self.now_time - self.time_stamp))
        if self.now_time - self.time_stamp >= 0.03:  # 时间检测
            if track_angle - self.deg >= 2:  # 角度检测
                return True
            else:
                print('角度过小，忽略执行')
                return False
        else:
            print('冷却中...')
            return False

    def run(self, angle):
        if self.track(angle):
            pwm.set_servo_angle(self.cel, angle)
        self.deg = angle

    def information(self):
        print(self.deg)
        print(self.time_stamp)


test = Servo(0)
if __name__ == '__main__':
    test.information()
    test.run(90)
    test_time = random.uniform(0, 1)
    print('等待时间'+str(test_time))
    test.run(180)
