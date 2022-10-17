import time
from multiprocessing import Process, Manager
from PIL import Image
import numpy as np
import cv2
from imutils import paths


def resize_img_keep_ratio(img_name, target_size):
    '''
    1.resize图片，先计算最长边的resize的比例，然后按照该比例resize。
    2.计算四个边需要padding的像素宽度，然后padding
    '''
    try:
        # 用cv2&numpy打开，这样可以读取中文路径
        # img = cv2.imdecode(np.fromfile(img_name, dtype=np.uint8), -1)  # 读入完整的图片
        # 使用PIL读取图片，防止中文路径和png格式的报错
        im = Image.open(img_name)

        # 转化为数组的格式
        im_array = np.array(im)
    # 报错提示
    except Exception as e:
        print(img_name, e)

    old_size = im_array.shape[:2]
    ratio = min(float(target_size[i]) / (old_size[i]) for i in range(len(old_size)))  # 取长和宽的最小值
    new_size = tuple([int(i * ratio) for i in old_size])
    img = cv2.resize(im_array, (new_size[1], new_size[0]), interpolation=cv2.INTER_CUBIC)  # 注意插值算法
    pad_w = target_size[1] - new_size[1]
    pad_h = target_size[0] - new_size[0]
    top, bottom = pad_h // 2, pad_h - (pad_h // 2)
    left, right = pad_w // 2, pad_w - (pad_w // 2)
    # 填充图片，黑边填充        cv2.copyMakeBorder()：给图片添加边框,cv2.BORDER_CONSTANT:固定值填充，（top, bottom, left, right）：上下左右要填的像素数
    img_new = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, None, (0, 0, 0))

    if img_name.count('.png') == 1 or img_new.shape[-1] == 4:
        return cv2.cvtColor(img_new, cv2.COLOR_RGBA2RGB)     # 从RGB图像中去除alpha通道
    return img_new


def getData(num, paths, return_dict, config):

    # 获取数据
    Data = []
    for img_path in paths:
        img = resize_img_keep_ratio(img_path, (config["imageResize"][0], config["imageResize"][1]))   # resize图像
        Data.append(img)
    Data = np.array(Data, dtype=np.float)  # 列表转元组
    Data /= 255.0
    return_dict[num] = Data   # 存储每个进程编号及需要处理的图像


def readImgMultiProcessing(imgpaths, corenum, config):
    # 路径划分
    # E:/demo_image/computer_obtain/82bf39b0-de2e-473d-9024-49ac901b9ca8_67.png
    lenPerSt = int(len(imgpaths)/corenum+1)   # （150/10+1） 16
    paths = []
    for i in range(corenum):
        paths.append(imgpaths[i * lenPerSt:(i + 1) * lenPerSt])   # 给每个进程分配任务（0~15，16~31，32~47....）  [[],[]...]
    # 多进程返回值接收器,manager实现进程间共享数据，Manager()返回一个manager对象，它控制一个服务器进程，该进程会管理python对象并允许其他进程通过代理的方式来操作这些对象，manager对象支持多种类型
    manager = Manager()
    # multiprocessing.Manager().dict()可以对简单字典进行传参并且可修改，注意：对于嵌套字典，在主进程内修改最内层的字典值，修改无效
    return_dict = manager.dict()
    return_list = manager.list()
    jobs = []

    # 执行进程
    for i in range(corenum):
        s = time.time()
        p = Process(target=getData, args=(str(i), paths[i], return_dict, config))   # 创建进程
        jobs.append(p)
        p.start()
        e = time.time()
        print(f'第{i+1}个进程：', e-s)
        return_list.append(e-s)

    for proc in jobs:
        proc.join()  # 阻塞主进程，等子进程执行结束后再进行

    # 合并数据
    data_con = np.asarray((list(return_dict['0'])))
    for i in range(1, corenum):
        x = np.asarray((list(return_dict[str(i)])))
        if int(x.shape[0]) > 0:
            data_con = np.concatenate((data_con, x))
    return data_con


if __name__ == '__main__':
    imgPath = 'E:/demo_image/computer_obtain/'
    # 使用imutils.paths模块中的list_images()方法可以获取当前目录下的图片路径
    imagePaths = sorted(list(paths.list_images(imgPath)))   # 获取所有图像的路径（包括路径+文件名）并排序

    config = {"epochs": 10, "batch_size": 128, "imageResize": (480, 480)}
    coreNum = 10   # 进程数
    start = time.time()
    data = readImgMultiProcessing(imagePaths, coreNum, config)
    end = time.time()
    print('总体耗时', end-start)
    print('data.shape:', data.shape)




