import cv2, os, sys, json
import threading
from queue import Queue
from PyQt5 import QtCore, QtWidgets

from multi_process.qt_page.camera_open import Ui_Form
from multi_process.qt_page.open_camera import Ui_MainWindow
from multi_process.multithread_main import write_img, read_img


class Open_Camera(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(Open_Camera, self).__init__()
        self.setupUi(self)  # 创建窗体对象
        self.init()
        # self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.photo_flag = 0
        self.label.setScaledContents(True)  # 图片自适应
        # self.label_2.setScaledContents(True)  # 图片自适应

    def init(self):
        # 定时器让其定时读取显示图片
        # self.camera_timer = QTimer()   # 定义定时器，用于控制显示视频的帧率
        # self.camera_timer.timeout.connect(self.show_image)
        # 打开摄像头
        self.pushButton_4.clicked.connect(self.open_camera)
        # # 拍照
        # self.pushButton_3.clicked.connect(self.taking_pictures)
        # 关闭摄像头
        self.pushButton_3.clicked.connect(self.close_camera)
        # # 导入图片
        # self.pushButton_5.clicked.connect(self.loadphoto)

    '''程序开始'''
    def open_camera(self):
        save_path = 'E:/demo_image/write_img/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        with open('./config.json', 'r', encoding='utf-8') as c:
            config = c.read()
            config = json.loads(config)

        rlock = threading.RLock()
        queue = Queue(config["queue_count"])
        r_record = []

        # 入队
        w = threading.Thread(name="write_img", target=write_img, args=(queue, config))
        w.start()

        # 出队
        for i in range(config["read_thread_count"]):
            r = threading.Thread(name=f'read_img_{i}', target=read_img, args=(queue, rlock, config, save_path))
            r.start()
            r_record.append(r)

        # 主线程等到子线程执行结束之后再继续
        w.join()
        for r in r_record:
            r.join()

    '''结束程序'''
    def close_camera(self):
        # self.cap.release()  # 释放摄像头
        # self.label.clear()  # 清除label组件上的图片
        # self.label_2.clear()  # 清除label组件上的图片
        # self.label.setText("摄像头")
        # while self.cap.isOpened():
        #     self.cap.release()  # 释放摄像头
        #     self.label.clear()  # 清除label组件上的图片
        #     self.label_2.clear()  # 清除label组件上的图片
        print('退出系统')

        sys.exit(0)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应分辨率
    app = QtWidgets.QApplication(sys.argv)  # 实例化一个应用对象
    ui = Open_Camera()
    ui.show()   # 显示界面
    sys.exit(app.exec_())  # 确保主循环安全退出





