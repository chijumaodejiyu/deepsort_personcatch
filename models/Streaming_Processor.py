import numpy as np
import cv2
import threading
from copy import deepcopy

thread_lock = threading.Lock()  # 创建一个线程锁
thread_exit = False  # 线程退出标志


class capThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(capThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):
        global thread_exit
        cap = cv2.VideoCapture(self.camera_id)  # 打开相机
        while not thread_exit:
            ret, frame = cap.read()  # 读取相机帧
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度
            if ret:
                frame = cv2.resize(frame, (width, height))  # 调整帧大小
                thread_lock.acquire()  # 获取线程锁
                self.frame = frame  # 更新帧
                thread_lock.release()  # 释放线程锁
            else:
                thread_exit = True  # 读取失败时退出线程
        cap.release()  # 释放相机


# 示例
def main():
    global thread_exit
    camera_id = 0
    img_height = 480
    img_width = 640
    thread = capThread(camera_id, img_height, img_width)  # 创建线程对象
    thread.start()  # 启动线程
    while not thread_exit:
        thread_lock.acquire()  # 获取线程锁
        frame = thread.get_frame()  # 获取线程中的图像帧
        thread_lock.release()  # 释放线程锁
        cv2.imshow('Video', frame)  # 显示图像帧
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按下q键退出
            thread_exit = True  # 设置退出标志
    thread.join()  # 等待线程结束


if __name__ == "__main__":
    main()
