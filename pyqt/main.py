# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera_open.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(486, 408)
        self.label_camera = QtWidgets.QLabel(Form)
        self.label_camera.setGeometry(QtCore.QRect(50, 50, 211, 141))
        self.label_camera.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 20pt \"摄像头\";")
        self.label_camera.setTextFormat(QtCore.Qt.AutoText)
        self.label_camera.setObjectName("label_camera")
        self.label_image = QtWidgets.QLabel(Form)
        self.label_image.setGeometry(QtCore.QRect(50, 220, 211, 141))
        self.label_image.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-bottom-color: rgb(0, 0, 0);\n"
"font: 20pt \"图片显示\";")
        self.label_image.setObjectName("label_image")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(310, 110, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 160, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 220, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(310, 280, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_camera.setWhatsThis(_translate("Form", "<html><head/><body><p align=\"center\">摄像头</p></body></html>"))
        self.label_camera.setText(_translate("Form", "<html><head/><body><p align=\"center\">摄像头</p></body></html>"))
        self.label_image.setText(_translate("Form", "<html><head/><body><p align=\"center\">图像显示</p></body></html>"))
        self.pushButton.setText(_translate("Form", "获取相机信息"))
        self.pushButton_2.setText(_translate("Form", "打开摄像头"))
        self.pushButton_3.setText(_translate("Form", "拍照"))
        self.pushButton_4.setText(_translate("Form", "关闭摄像头"))