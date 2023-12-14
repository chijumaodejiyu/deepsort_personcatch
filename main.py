import time
import tracker
from detector import Detector
from models.cap_track import CapTracker
import cv2

if __name__ == '__main__':
    # 初始化 detector
    detector = Detector()
    capture = cv2.VideoCapture(0)
    # 初始化舵机
    trackers = CapTracker((3, -1), (0, 0), dxy_p=(0.15, 0.15))
    while True:
        start = time.perf_counter()

        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            print("Fail to get photo.")
            continue
        # 画面矫正
        # 0: 竖直调转
        # 1: 水平掉转
        im = cv2.flip(im, 0)
        # 画面大小传输
        if trackers.screen_shape == (0, 0):
            trackers.set_screen_shape(im.shape)
            print(trackers.dxy)
            print(trackers.screen_shape)
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
        # center_xy = None
        # center_list = {}
        # 追踪
        if len(list_bboxs) > 0:
            item_bbox = list_bboxs[0]
            trackers.track(item_bbox)

            pass
        else:
            pass
        cv2.imshow('demo', output_image_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        # print("fps:{}".format(1 / (time.perf_counter() - start)))
        # print('center:'+str(center_list))

        pass
    pass
    capture.release()
    cv2.destroyAllWindows()
