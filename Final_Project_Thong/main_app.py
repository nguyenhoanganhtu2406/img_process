import sys
import cv2 as cv

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QFileDialog, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon

from img_process import ImageProcessing as IP

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.filename = ""
        super(Ui_MainWindow, self).__init__()
        uic.loadUi("ui.ui", self)
        self.setWindowTitle("Image Processing")
        self.show()
        self.init()
        self.ip = ""
        self.toolbar = False
        self.img_exist = False
        self.setWindowIcon(QIcon("icon/mainicon.png"))
        self.curImg = False
        QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def init(self):
        #bắt các sự kiện action
        self.act_open_img.triggered.connect(self.open_image)
        self.act_chapter3.triggered.connect(self.chapter3_click)
        self.act_chapter5.triggered.connect(self.chapter5_click)
        self.act_chapter8.triggered.connect(self.chapter8_click)
        self.act_save.triggered.connect(self.save_img)

        self.rotation_inp.valueChanged.connect(self.rotation)
        self.scaling_inp.valueChanged.connect(self.scaling)
        self.tranX_inp.valueChanged.connect(self.getTranX)
        self.tranY_inp.valueChanged.connect(self.getTranY)
        self.shear_inp.valueChanged.connect(self.shearing)

     
        self.log_inp.valueChanged.connect(self.log)
        self.gamma_inp.valueChanged.connect(self.gamma)

     
        self.median_inp.valueChanged.connect(self.median)
        self.bila_inp.valueChanged.connect(self.bilateral)
        self.gaussian_inp.valueChanged.connect(self.gaussian)
        self.blur_inp.valueChanged.connect(self.blur)


    def save_img(self):
        img = self.curImg
        # size đến tên hình =36
        s = self.filename[0]
        print(s)
        photoName = ""
        for i in range(len(s) - 1, 0, -1):
            if s[i] == '/':
                photoName = s[i + 1:len(s) - 4]
                photoName = photoName + "_Changed" + s[len(s) - 4:]
                break

        q = QMessageBox.question(self, "Xác nhận", "Lưu ảnh này?", QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        if (q == QMessageBox.Yes):
            cv.imwrite(photoName, img)
            QMessageBox.about(self, "Thông báo", "Lưu thành công")

    def open_image(self):
        self.filename = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", 
                            "Images File(*.jpg; *.jpeg; *.png, *.tif);;Python Files (*.py)")
        if(self.filename[0] != ''):
            width = self.labelOriginal.width()
            height = self.labelOriginal.height()
            self.labelOriginal.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            self.labelChanged.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            width = self.labelOriginal.width()
            height = self.labelOriginal.height()
            self.ip = IP(self.filename[0], width, height)
            self.img_exist = True
            self.geo_enable()
            self.spatial_enable()
            self.gray_enable()

    def geo_enable(self):
        if (self.img_exist == True):
            self.chapter2_group.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def spatial_enable(self):
        if (self.img_exist == True):
            self.chapter3_group.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def gray_enable(self):
        if (self.img_exist == True):
            self.chapter4_group.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def bind_to_label(self, changed_img):
        qformat = QImage.Format_RGB888
        self.curImg=changed_img

        if len(changed_img.shape) == 3:
            if (changed_img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(changed_img, changed_img.shape[1], changed_img.shape[0], changed_img.shape[1]*3, qformat).rgbSwapped()
        self.labelChanged.setPixmap(QPixmap.fromImage(img))
        self.labelChanged.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


    def negative(self):
        res = self.ip.negative()
        self.bind_to_label(res)

    def histogram(self):
        res = self.ip.histogram()
        self.bind_to_label(res)

    def adapt_histogram(self):
        res = self.ip.adapt_histogram()
        self.bind_to_label(res)

    def log(self, m):
        self.log_val.setText(str(m))
        res = self.ip.log(m)
        self.bind_to_label(res)

    def gamma(self, m):
        self.gamma_val.setText(str("{0:.1f}".format(round(m*0.1, 1))))
        res = self.ip.gamma(m*0.1)
        self.bind_to_label(res)

    def getTranX(self, x):
        self.tranX_val.setText(str(x))
        self.translation()

    def getTranY(self, y):
        self.tranY_val.setText(str(y))
        self.translation()

    def translation(self):
        x = int(self.tranX_val.text())
        y = int(self.tranY_val.text())
        res = self.ip.translation(x, y)
        self.bind_to_label(res)

    def scaling(self, size):
        res = self.ip.scaling(size)
        self.scaling_val.setText(str(size) + "%")
        self.bind_to_label(res)

    def rotation(self, angle):
        self.rotation_val.setText(str(angle)+"°")
        res = self.ip.rotation(angle)
        self.bind_to_label(res)

    def shearing(self, m):
        self.shear_val.setText(str(m))
        res = self.ip.shearing(m)
        self.bind_to_label(res)

    #Chuong4
    def blur(self, n):
        self.blur_val.setText(str(n * 2 - 1))
        size = int(self.blur_val.text())
        res = self.ip.blur(size)
        self.bind_to_label(res)

    def gaussian(self, n):
        self.gaussian_val.setText(str(n * 2 - 1))
        size = int(self.gaussian_val.text())
        res = self.ip.gaussian(size)
        self.bind_to_label(res)

    def median(self, n):
        self.median_val.setText(str(n*2-1))
        size = int(self.median_val.text())
        res = self.ip.median(size)
        self.bind_to_label(res)

    def bilateral(self, sigma):
        self.bila_val.setText(str(sigma))
        size = int(self.bila_val.text())
        res = self.ip.bilateral(sigma)
        self.bind_to_label(res)

    def fourier(self):
        res=self.ip.fourier()
        #self.bind_to_label(res)

    def highPass(self):
        res=self.ip.highPassGaussian()
        self.bind_to_label(res)

    def canny(self):
        res=self.ip.canny()
        self.bind_to_label(res)

    #chương 8
    def sobelx(self):
        res = self.ip.sobelX()
        self.bind_to_label(res)
    def sobely(self):
        res = self.ip.sobelY()
        self.bind_to_label(res)
    def laplacian(self):
        res = self.ip.laplacian()
        self.bind_to_label(res)

    def chapter3_click(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()
            
            act_negative = QAction(QIcon(), 'Negative', self)
            act_negative.triggered.connect(self.negative)

            act_histogram = QAction(QIcon(), 'Histogram', self)
            act_histogram.triggered.connect(self.histogram)

            act_adapt_histogram = QAction(QIcon(), 'Adaptive Histogram', self)
            act_adapt_histogram.triggered.connect(self.adapt_histogram)

            self.toolbar.clear()
            self.toolbar.addAction(act_negative)
            self.toolbar.addAction(act_histogram)
            self.toolbar.addAction(act_adapt_histogram)
            self.chuong3Group.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def chapter5_click(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actionFourier = QAction('Fourier', self)
            actionFourier.triggered.connect(self.fourier)

            actionHighPass = QAction('High-Pass Filter', self)
            actionHighPass.triggered.connect(self.highPass)

            #self.toolbar.addAction(actionFourier)
            self.toolbar.addAction(actionHighPass)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def chapter8_click(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            act_sobelX = QAction(QIcon(), 'SobelX', self)
            act_sobelX.triggered.connect(self.sobelx)
            self.toolbar.addAction(act_sobelX)

            act_sobelY = QAction(QIcon(), 'SobelY', self)
            act_sobelY.triggered.connect(self.sobely)
            self.toolbar.addAction(act_sobelY)

            act_laplacian = QAction(QIcon(), 'Lapcian', self)
            act_laplacian.triggered.connect(self.laplacian)
            self.toolbar.addAction(act_laplacian)

            act_canny = QAction(QIcon(), 'Canny', self)
            act_canny.triggered.connect(self.canny)
            self.toolbar.addAction(act_canny)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    win = Ui_MainWindow()
    sys.exit(a.exec_())

