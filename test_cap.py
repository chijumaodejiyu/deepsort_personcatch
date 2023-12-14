import cv2


# 数据定义
channel = 0

# channel = int(input("Type the number of capture:\n"))

# 摄像头初始化
cap = cv2.VideoCapture(channel)

while True:
    # 获取画面
    _, image = cap.read()
    # 画面矫正
    image = cv2.flip(image, 0)
    # 展示画面
    cv2.imshow('Picture', image)
    # 等待按键
    key = cv2.waitKey(1)
    # 退出
    if key == 0x1b:
        print("Test Over!")
        break
