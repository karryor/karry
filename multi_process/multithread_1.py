'''
1.创建多线程，写入：一个线程（隔段时间写入一次），处理：多个线程
2.加锁(Lock碰到嵌套会产生死锁，所以用RLck)
3.加队列（多个线程用的一个队列）
4.添加配置文件：config：队列最大存放量，读取队列线程数，线程数，网络模型输入图像尺寸，摄像头url，图像写入间隔时间
5.加上人脸检测，检测后保存图像

帧率：25

耗时：
读取或写入图片耗时（put或get）：0.0
人脸检测所需时间：0.034781694412231445
读取图片+人脸检测：0.034781694412231445
读取图片+人脸检测+保存处理后的照片：0.05399608612060547
保存处理后的照片：0.019214391708374
'''

import threading
import os
import cv2
import time
from datetime import datetime
from queue import Queue
import json
from multi_process.face_detection import signal_detect


save_path = 'E:/demo_image/write_img/'
if not os.path.exists(save_path):
    os.mkdir(save_path)
img_list = []


class Write_img(threading.Thread):
    def __init__(self, name, queue, rlock, config):
        threading.Thread.__init__(self, name=name)
        self.queue = queue
        self.rlock = rlock
        self.config = config

    def run(self):
        cap = cv2.VideoCapture(self.config["camera_url"])
        if not cap.isOpened():
            print('camera open failed')

        while True:
            print('\n当前写入线程name：', self.getName())
            ret, frame = cap.read()
            if not queue.full():
                self.rlock.acquire()
                s = time.time()
                self.queue.put(frame)
                e = time.time()
                self.rlock.release()
                print('-----写入一张图片所需时间-------', e-s)
                print('------当前时间-----', datetime.now())
                print('当前队列中消息数量：', queue.qsize())
                time.sleep(self.config["write_interval"])  # 每隔1秒读取一次图片
            else:
                print('-----队列已满，等待------')
                time.sleep(self.config["write_wait_time"])
                continue
            print('-----释放锁------')


class Read_img(threading.Thread):
    def __init__(self, name, queue, rlock, config):
        threading.Thread.__init__(self, name=name)  # ?????
        self.queue = queue
        self.rlock = rlock
        self.config = config

    def run(self):
        while True:
            self.rlock.acquire()
            print('\n当前读取线程name：', self.getName())
            if not queue.empty():
                s_1 = time.time()
                img = self.queue.get()
                ssss = time.time()
                print('get图像所需时间', ssss-s_1)
                print('当前队列中消息数量：', queue.qsize())
                '''
                引用图像预处理，传入到网络模型进行处理
                '''
                # 图像处理
                s = time.time()
                img = signal_detect(img)
                e = time.time()
                print('------人脸检测所需时间--------', e-s)
                now = datetime.now()
                timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
                cv2.imwrite(save_path + timestr + '_' + str(queue.qsize()) + '.png', img)
                end = time.time()
                print('-----读取并人脸检测总时间--------', e-s_1)
                print('-----读取、人脸检测和保存图片总时间--------', end-s_1)
            else:
                self.rlock.release()
                print('队列为空,等待')
                time.sleep(self.config["read_wait_time"])
                continue
            self.rlock.release()


if __name__ == '__main__':
    with open('./config.json', 'r', encoding='utf-8') as c:
        config = c.read()
        conf = json.loads(config)
        c.close()

    queue = Queue(conf["queue_count"])
    r_record = []
    rlock = threading.RLock()

    # 入队
    w = Write_img(f"write_img", queue, rlock, conf)
    w.start()
    # 出队
    for i in range(conf["read_thread_count"]):
        t = Read_img(f'read_img_{i}', queue, rlock, conf)
        t.start()
        r_record.append(t)

    # 主线程等到子线程执行结束之后再继续
    w.join()
    for r in r_record:
        r.join()



