from datetime import datetime

import cv2

import uuid
import time
import os


'''
rtsp://[username]:[passwd]@[ip]:[port]/[codec]/[channel]/[subtype]/av_stream
codec：编码类型：有h264、MPEG-4、mpeg4这几种
channel：通道号，起始为1
subtype：码流类型，主码流为main,子码流为sub
主码流：（本地录像）
rtsp://admin:12345@192.168.1.64:554/h264/ch1/main/av_stream
子码流：（网络传输）
rtsp://admin:12345@192.168.1.64:554/h264/ch1/sub/av_stream


cap.isOpen
'''


def test_download():
    # cv2.VideoCapture：读取视频或摄像头图片；打开指定路径下的摄像头，参数为0时是笔记本内置摄像头
    cap = cv2.VideoCapture("rtsp://admin:kbzn2021@192.168.2.64:554/h264/ch1/sub/av_stream")
    # cap = cv2.VideoCapture("E:/demo_image/hkws/192.168.2.64_01_20221010112838418.mp4")
    # cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("camera open failed")

    # frame_s = cap.get(cv2.CAP_PROP_FPS)  # opencv不支持h264视频编码，可能重新编译ffmpeg能够识别opencv
    frame_s = 25
    # 设置视频格式，VideoWriter_fourcc:用于指定视频的编码格式，cv2.VideoWriter_fourcc('m', 'p', '4', 'v')：文件扩展名.mp4
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # 获取视频的宽度(cv2.CAP_PROP_FRAME_WIDTH)和高度（cv2.CAP_PROP_FRAME_HEIGHT）
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 从视频或摄像头中读取一帧，ret:返回是否成功（true/false），frame:读取的视频帧
    ret, frame = cap.read()

    # 设置保存时间为time_frame秒保存一次
    time_frame = frame_s * 2
    # print(time_frame)

    num = 0
    count = 1
    pathname = 'E:/demo_image/hkws/'
    if not os.path.exists(pathname):
        os.mkdir(pathname)

    while ret:
        if num == 0:
            # uuid.uuid4()   基于随机数   通过随机数生产uuid
            # time.time()以时间明明
            now = datetime.now()
            timestr = now.strftime('%Y_%m_%d_%H_%M_%S')
            filename = pathname + timestr+'_'+str(count)+'.mp4'

            # 创建视频流写入对象；参数：视频文件名，格式，每秒帧数，宽高，是否灰度
            print(filename)
            video_writer = cv2.VideoWriter(filename, fourcc, frame_s, size, True)
        ret, frame = cap.read()

        cv2.imshow("frame", frame)
        cv2.waitKey(2)

        # 保存每一帧的图像
        cv2.imwrite(filename[:-4]+'_'+str(num)+'.png', frame)
        #  img = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_LINEAR)

        video_writer.write(frame)
        num = num + 1
        # 保存前count*time_frame秒的视频
        if count == 3 and num == time_frame:
            video_writer.release()
            break

        # 当num == time_frame时，保存一次视频，视频时长为time_frame秒
        if num == time_frame:
            video_writer.release()
            num = 0
            count += 1
            continue

    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    test_download()














