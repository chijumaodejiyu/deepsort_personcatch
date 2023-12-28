from models import tracker
from models.detector import Detector
from models.cap_module import CapFinder
from models.data_process import list_bboxes2dict_bboxes
from models.Regional_monitoring import *
from Gui import Gui
import cv2


if __name__ == '__main__':
    # 初始化 detector
    detector = Detector()
    finder_cap = cv2.VideoCapture(0)
    tracker_cap = cv2.VideoCapture(1)
    # 初始化追踪器
    finder = CapFinder((3, -1), (0, 0), (120, 90))
    # 初始化Gui界面
    gui = Gui()
    # 初始化数据
    track_id = ''
    ids = []
    # 初始化监测器
    monitor = Regional_monitoring()
    while True:
        # start = time.perf_counter()

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
        # pic = cv2.flip(pic, 0)
        # 画面大小传输
        if finder.screen_shape == (0, 0):
            finder.screen_shape = im.shape[: -1]
            print(finder.screen_shape)
        width = int(finder_cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
        height = int(finder_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度

        # 调整至摄像头实际尺寸
        im = cv2.resize(im, (width, height))

        gui.update()
        event = gui.event

        list_bboxes = []
        dict_bboxes = {}
        bboxes = detector.detect(im)

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxes = tracker.update(bboxes, im)
            dict_bboxes = list_bboxes2dict_bboxes(list_bboxes)
            # 框绘制
            output_image_frame = tracker.draw_bboxes(im, list_bboxes, line_thickness=None)
            output_image_frame = monitor.draw(output_image_frame)
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
            output_image_frame = monitor.draw(output_image_frame)

        ids = list(dict_bboxes.keys())
        gui.add_id(ids)
        track_id = gui.get_id()

        # 追踪
        if len(dict_bboxes.items()) > 0:
            if track_id in dict_bboxes.keys():
                print(ids)
                print(track_id)
                item_bbox = dict_bboxes[str(track_id)]
                finder.track(item_bbox)
                # 危险区域判定
                monitor_id = gui.get_id()
                if monitor.check(item_bbox):  # 侦测到box处于危险区域
                    print(str(monitor_id)+'号目标处于危险区域')
                    pass
        gui.update_image('-FINDER-', output_image_frame)
        gui.update_image('-TRACKER-', pic)
        if event in ('Exit', None):
            break
        # print("fps:{}".format(1 / (time.perf_counter() - start)))
    finder_cap.release()
    tracker_cap.release()
    cv2.destroyAllWindows()
