from models import tracker
from models.detector import Detector
from models.cap_module import CapFinder
from models.data_process import list_bboxes2dict_bboxes
from models.Regional_monitoring import Regional_monitoring
import cv2


def main():# 初始化 detector
    detector = Detector()
    finder_cap = cv2.VideoCapture(1)
    tracker_cap = cv2.VideoCapture(0)
    # 初始化追踪器
    finder = CapFinder((3, -1), (0, 0), (90, 90))
    # 初始化检测器
    monitor = Regional_monitoring()
    # 初始化数据
    track_id = -1
    track_ids = []
    ids = []
    while True:
        # start = time.perf_counter()
        print(track_ids)
        track_ids = []

        # 读取每帧图片
        _, im = finder_cap.read()
        _, pic = tracker_cap.read()
        if im is None:
            print("Fail to get photo.")
            continue
        # 画面矫正
        # 0: 竖直调转
        # 1: 水平掉转
        im = cv2.flip(im, 0)
        pic = cv2.flip(pic, 0)
        # 画面大小传输
        if finder.screen_shape == (0, 0):
            finder.screen_shape = im.shape[: -1]
            print(finder.screen_shape)
        width = int(finder_cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
        height = int(finder_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度

        # 调整至摄像头实际尺寸
        im = cv2.resize(im, (width, height))

        list_bboxes = []
        dict_bboxes = {}
        bboxes = detector.detect(im)

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxes = tracker.update(bboxes, im)
            dict_bboxes = list_bboxes2dict_bboxes(list_bboxes)
            # 框绘制
            output_image_frame = tracker.draw_bboxes(im, list_bboxes, line_thickness=None)
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        if len(dict_bboxes.items()) > 0:
            # 检测
            for id_, item_bbox in dict_bboxes.items():
                # if monitor.check(item_bbox):
                #     track_ids.append(id_)
                track_ids.append(id_)

        if len(track_ids) > 0:
            # 追踪
            if track_id not in track_ids:
                track_id = track_ids[0]
            item_bbox = dict_bboxes[str(track_id)]
            finder.track(item_bbox)
        cv2.imshow('demo', output_image_frame)
        if pic is not None:
            cv2.imshow('picture', pic)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        # print("fps:{}".format(1 / (time.perf_counter() - start)))
    finder_cap.release()
    tracker_cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
