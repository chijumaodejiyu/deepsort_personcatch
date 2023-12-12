import numpy as np
import time
import tracker
from detector import Detector
from Servo_control import Servo
import cv2

if __name__ == '__main__':
    # 初始化 detector
    detector = Detector()
    capture = cv2.VideoCapture(0)
    # 初始化舵机
    servo = Servo(3)
    while True:
        start = time.perf_counter()

        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度

        # 调整至摄像头实际尺寸
        im = cv2.resize(im, (width, height))

        list_bboxs = []
        bboxes = detector.detect(im)

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)
            # 框绘制
            output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass
        center_xy = None
        center_list = {}
        if len(list_bboxs) > 0:
            for item_bbox in list_bboxs:
                x1, y1, x2, y2, _, track_id = item_bbox
                center_xy = str(int((x1 + x2)/2))+','+str(int((y1 + y2)/2))
                y_rate = int((y1 + y2)/2)/int(width)
                target_deg = int(180*y_rate)
                servo.run(target_deg)
                # while int((y1+y2)/2) != int((width+height)/2):
                #     if int((y1+y2)/2) == int((width+height)/2):
                #         break
                #     elif int((y1+y2)/2) < int((width+height)/2):
                #         servo.run(0)
                #     elif int((y1+y2)/2) > int((width+height)/2):
                #         servo.run(180)
                #     else:
                #         break
                center_list[track_id] = center_xy

            pass
        else:
            pass
        cv2.imshow('demo', output_image_frame)
        cv2.waitKey(1)
        key = cv2.waitKey(24)
        if key == ord('q'):
            break
        print("fps:{}".format(1 / (time.perf_counter() - start)))
        print('center:'+str(center_list))

        pass
    pass
    capture.release()
    cv2.destroyAllWindows()
