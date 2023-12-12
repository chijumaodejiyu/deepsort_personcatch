#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from pca9685 import PCA9685

pwm = PCA9685(0x40, debug=True)  # 对象初始化，指定IIC地址
pwm.setPWMFreq(50)  # 设置PWM的频率


class Servo:
    def __init__(self, cel):
        self.nextAngle = None
        self.cel = cel  # 通道设置
        self.deg = 0
        pwm.set_servo_angle(cel, 0)  # 重置舵机

    def run(self, angle):
        if angle <= 180:
            pwm.set_servo_angle(self.cel, angle)  # 舵机转动
            self.deg = angle  # 记忆当前角度
        else:
            print('超出攻角限制')
            pass
        time.sleep(0.05)  # 休眠

    def information(self):
        print(self.deg)
