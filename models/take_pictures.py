import cv2
import time
import datetime
import os

# 初始化摄像头
channel = 0
cap = cv2.VideoCapture(channel)

if not os.path.exists("./img"):
    os.mkdir("./img")

while True:
    # 读取摄像头的画面
    ret, frame = cap.read()
    frame = cv2.flip(frame, 0)
    if not ret:
        print("无法获取摄像头画面，退出。")
        break

        # 显示画面
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    # 检测是否按下空格或q键
    if key == ord(' '):
        # 获取当前时间（精确到毫秒）
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        path = f"./img/{now}.jpg"
        cv2.imwrite(path, frame)
        print(f"图片已保存至{path}")
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
