'''
海康IPcamera rtsp地址和格式：
rtsp://[username]:[password]@[ip]:[port]/[codec]/[channel]/[subtype]/av_stream

codec：有h264、MPEG-4、mpeg4这几种
channel: 通道号，起始为1。例如通道1，则为ch1
subtype: 码流类型，主码流为main，辅码流为sub

'''

import cv2


def main():
    output_path = 'E:/demo_image/output.avi'
    vc = cv2.VideoCapture('rtsp://admin:kbzn2021@192.168.2.64:554/h264/ch1/sub/av_stream')
    ret, frame = vc.read()
    w = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vc.get(cv2.CAP_PROP_FPS)
    print(fps)
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    # fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    # fourcc = cv2.VideoWriter_fourcc('H', 'E', 'V', 'C')
    vw = cv2.VideoWriter(output_path, fourcc, fps, (w, h), True)
    while ret:
        vw.write(frame)
        ret, frame = vc.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return -1


if __name__ == '__main__':
    main()



