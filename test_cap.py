import cv2


# 数据定义
channels = (0, 1)

# channel = int(input("Type the number of capture:\n"))

# 摄像头初始化
caps = {}
for channel in channels:
    cap = cv2.VideoCapture(channel)
    caps[str(channel)] = cap

while True:
    # 获取画面
    for channel, cap in caps.items():
        _, image = cap.read()
        # 画面矫正
        image = cv2.flip(image, 0)
        # 展示画面
        cv2.imshow(f'Capture{channel}', image)
    # 等待按键
    key = cv2.waitKey(1)
    # 退出
    if key == 0x1b:
        print("Test Over!")
        break

for channel, cap in caps.items():
    cap.release()
    print(f'Capture{channel} was released.')
