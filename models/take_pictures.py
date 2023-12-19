import cv2
import time
import datetime
import os

# 初始化摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取摄像头的画面
    ret, frame = cap.read()
    if not ret:
        print("无法获取摄像头画面，退出。")
        break

        # 显示画面
    cv2.imshow("Camera", frame)

    # 检测是否按下空格或q键
    if cv2.waitKey(1) & 0xFF == ord(' ') or cv2.waitKey(1) & 0xFF == ord('q'):
        # 获取当前时间（精确到毫秒）
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        cv2.imwrite(os.path.join('pytorch/img', f'{now}.jpg'), frame)
        print(f"图片已保存至img/{now}.jpg")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
cap.release()
