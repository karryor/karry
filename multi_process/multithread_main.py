import threading
import os
import cv2
import time
from datetime import datetime
from queue import Queue
import json
import numpy as np
from multi_process.face_detection import signal_detect


def resize_img(img, config):
    old_size = img.shape[:2]  # shape:(h,w,channel)
    target_size = (config["imageResize"][0], config["imageResize"][1])
    print('target_size', target_size)
    ratio = min(float(target_size[i]) / (old_size[i]) for i in range(len(old_size)))  # 取比例最小值
    print('ratio', ratio)
    new_size = tuple([int(i * ratio) for i in old_size])
    print('old_size', old_size)
    print('new_size', new_size)
    print(img.shape)
    img = cv2.resize(img, (new_size[1], new_size[0]), interpolation=cv2.INTER_CUBIC)  # 注意插值算法   resize(img,(w,h),method)
    pad_w = target_size[1] - new_size[1]
    pad_h = target_size[0] - new_size[0]
    top, bottom = pad_h // 2, pad_h - (pad_h // 2)
    left, right = pad_w // 2, pad_w - (pad_w // 2)
    # 填充图片，黑边填充        cv2.copyMakeBorder()：给图片添加边框,cv2.BORDER_CONSTANT:固定值填充，（top, bottom, left, right）：上下左右要填的像素数
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, None, (0, 0, 0))
    img_new = np.array(img, dtype=float)
    # img_new /= 255.0   # 归一化
    img_list.append(img_new)
    return img_new


def write_img(queue, config):
    cap = cv2.VideoCapture(config["camera_url"])
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('camera open failed')

    while True:
        print('\n当前写入线程name：', threading.current_thread().name)
        ret, frame = cap.read()
        if not queue.full():
            queue.put(frame)
            print('------当前时间-----', datetime.now())
            print('当前队列中消息数量：', queue.qsize())
            time.sleep(config["write_interval"])  # 每隔1秒读取一次图片
        else:
            print('-----队列已满------')
            time.sleep(config["write_wait_time"])
            continue
        print('-----释放锁------')


def read_img(queue, rlock, config, save_path):
    while True:
        rlock.acquire()
        print('\n当前读取线程name：', threading.current_thread().name)
        print('-----加锁-------')
        if not queue.empty():
            img = queue.get()
            print('当前队列中消息数量：', queue.qsize())
            '''
            引用图像预处理，传入到网络模型进行处理
            '''
            # 图像预处理
            # img = resize_img(img, self.config)
            img = signal_detect(img)
            now = datetime.now()
            timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
            cv2.imwrite(save_path + timestr + '_' + str(queue.qsize()) + '.png', img)
        else:
            rlock.release()
            print('队列为空,释放锁')
            time.sleep(config["read_wait_time"])
            continue
        rlock.release()
        print('-----释放锁------')


if __name__ == '__main__':
    save_path = 'E:/demo_image/write_img/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    with open('./config.json', 'r', encoding='utf-8') as c:
        config = c.read()
        config = json.loads(config)

    img_list = []
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


