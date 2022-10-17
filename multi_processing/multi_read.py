from multi_processing.multi_process_read import readImgMultiProcessing
import os, random, time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imutils import paths
import numpy as np
seed = 300
random.seed(seed)
coreNum = 23
imgPath = ''
dataPath = ''
dataTestPath = ''
dataEncoderPath = r'babyFaceLabelEncoder.data'
config = {"epochs": 10, "batch_size": 128, 'useIDG':True, "imageResize": (600, 600), "lr": 1e-3}
if os.path.exists('tmp') == False:
    os.makedirs(r'tmp')
if __name__ == '__main__':
    if os.path.exists(dataPath) and os.path.exists(dataTestPath):
        (X_train, X_val, y_train, y_val) = readImgMultiProcessing.readFile(dataPath)
        (X_test, Y_test) = readImgMultiProcessing.readFile(dataTestPath)
        class_le = readImgMultiProcessing.readFile(dataEncoderPath)
    else:
        tst = time.time()
        class_le = LabelEncoder()
        class_le.fit(['睡', '醒'])
        # 读取所有的图片路径
        imagePaths = sorted(list(paths.list_images(imgPath)))
        # 读取婴儿醒睡的图片
        faceImagePaths = []
        for img_path in imagePaths:
            if(img_path.split(os.path.sep)[-2] == '睡' or img_path.split(os.path.sep)[-2] == '醒'):
                faceImagePaths.append(img_path)
        # 打乱顺序
        random.shuffle(faceImagePaths)
        # 这里就读取部分，内存不够
        # faceImagePaths = faceImagePaths[:234]
        # 用train_test_split划分 训练 验证 测试，注意：这里划分的是 路径
        trainImgPaths, testImgPaths = train_test_split(faceImagePaths, test_size=0.2, random_state=seed)
        trainImgPaths, valImgPaths = train_test_split(trainImgPaths,  test_size=0.2, random_state=seed)
        print('数据列表划分完成')
        # 图片
        X_train = readImgMultiProcessing.readImgMultiProcessing(trainImgPaths, coreNum, config)
        print('训练集读入完成')
        X_val = readImgMultiProcessing.readImgMultiProcessing(valImgPaths,   coreNum, config)
        print('验证集读入完成')
        X_test = readImgMultiProcessing.readImgMultiProcessing(testImgPaths,  coreNum, config)
        print('测试集读入完成')
        X_train = np.asarray(X_train, dtype=np.float) / 255.0
        print('训练集处理完成')
        X_val = np.asarray(X_val, dtype=np.float) / 255.0
        print('验证集处理完成')
        X_test = np.array(X_test, dtype=np.float) / 255.0
        print('测试集处理完成')
        # 婴儿表情的标签
        y_train = class_le.transform([x.split(os.path.sep)[-2] for x in trainImgPaths])
        y_val = class_le.transform([x.split(os.path.sep)[-2] for x in valImgPaths])
        Y_test = class_le.transform([x.split(os.path.sep)[-2] for x in testImgPaths])
        # 保存数据
        readImgMultiProcessing.toFile(class_le, dataEncoderPath)
        readImgMultiProcessing.toFile((X_train, X_val, y_train, y_val), dataPath)
        readImgMultiProcessing.toFile((X_test, Y_test), dataTestPath)
        print('数据集压缩成功，数据保存完毕')
        print(len(trainImgPaths), X_train.shape, len(y_train))
        print(len(valImgPaths), X_val.shape, len(y_val))
        print(len(testImgPaths), X_test.shape, len(Y_test))
        print('用时', time.time()-tst) # 934s



