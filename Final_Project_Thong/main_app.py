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
        self.actMoAnh.triggered.connect(self.moAnh)
        self.actMucXam.triggered.connect(self.mucXamTool)
        self.actTanSo.triggered.connect(self.tanSoTool)
        self.actCanh.triggered.connect(self.xacDinhCanhTool)
        self.actHoatHinh.triggered.connect(self.hoatHinhTool)
        self.actLuu.triggered.connect(self.luuAnh)

        self.inpGocQuay.valueChanged.connect(self.gocQuay)
        self.inpTiLe.valueChanged.connect(self.tiLe)
        self.inpX.valueChanged.connect(self.tinhTienX)
        self.inpY.valueChanged.connect(self.tinhTienY)
        self.inpBienDang.valueChanged.connect(self.bienDang)

     
        self.inpLog.valueChanged.connect(self.log)
        self.inpGamma.valueChanged.connect(self.gamma)

     
        self.inpMedian.valueChanged.connect(self.median)
        self.inpBila.valueChanged.connect(self.bilateral)
        self.inpGauss.valueChanged.connect(self.gaussian)
        self.inpBlur.valueChanged.connect(self.blur)


    def luuAnh(self):
        img = self.curImg
        s = self.filename[0]
        print(s)
        photoName = ""
        for i in range(len(s) - 1, 0, -1):
            if s[i] == '/':
                photoName = s[i + 1:len(s) - 4]
                photoName = photoName + "_XuLy" + s[len(s) - 4:]
                break

        q = QMessageBox.question(self, "Xác nhận", "Lưu ảnh này?", QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        if (q == QMessageBox.Yes):
            cv.imwrite(photoName, img)
            QMessageBox.about(self, "Thông báo", "Lưu thành công")

    def moAnh(self):
        self.filename = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", 
                            "Images File(*.jpg; *.jpeg; *.png, *.tif);;Python Files (*.py)")
        if(self.filename[0] != ''):
            width = self.lblGoc.width()
            height = self.lblGoc.height()
            self.lblGoc.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            self.lblXuLy.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            width = self.lblGoc.width()
            height = self.lblGoc.height()
            self.ip = IP(self.filename[0], width, height)
            self.img_exist = True
            self.hinhHocEnable()
            self.khongGianEnable()
            self.xamEnable()

    def hinhHocEnable(self):
        if (self.img_exist == True):
            self.grpHinhHoc.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def khongGianEnable(self):
        if (self.img_exist == True):
            self.grpXam.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def xamEnable(self):
        if (self.img_exist == True):
            self.grpKhongGian.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def ganVaoLabelXuLy(self, anhXuLy):
        qformat = QImage.Format_RGB888
        self.curImg=anhXuLy

        if len(anhXuLy.shape) == 3:
            if (anhXuLy.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(anhXuLy, anhXuLy.shape[1], anhXuLy.shape[0], anhXuLy.shape[1]*3, qformat).rgbSwapped()
        self.lblXuLy.setPixmap(QPixmap.fromImage(img))
        self.lblXuLy.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    #mức xám
    def negative(self):
        res = self.ip.negative()
        self.ganVaoLabelXuLy(res)

    def histogram(self):
        res = self.ip.histogram()
        self.ganVaoLabelXuLy(res)

    def adaptHistogram(self):
        res = self.ip.adaptHistogram()
        self.ganVaoLabelXuLy(res)

    def log(self, m):
        self.valLog.setText(str(m))
        res = self.ip.log(m)
        self.ganVaoLabelXuLy(res)

    def gamma(self, m):
        self.valGamma.setText(str("{0:.1f}".format(round(m*0.1, 1))))
        res = self.ip.gamma(m*0.1)
        self.ganVaoLabelXuLy(res)

    #hình học
    def tinhTienX(self, x):
        self.valX.setText(str(x))
        self.tinhTien()

    def tinhTienY(self, y):
        self.valY.setText(str(y))
        self.tinhTien()

    def tinhTien(self):
        x = int(self.valX.text())
        y = int(self.valY.text())
        res = self.ip.tinhTien(x, y)
        self.ganVaoLabelXuLy(res)

    def tiLe(self, size):
        res = self.ip.tiLe(size)
        self.scaling_val.setText(str(size) + "%")
        self.ganVaoLabelXuLy(res)

    def gocQuay(self, goc):
        self.valGocQuay.setText(str(goc)+"°")
        res = self.ip.gocQuay(goc)
        self.ganVaoLabelXuLy(res)

    def bienDang(self, m):
        self.valBienDang.setText(str(m))
        res = self.ip.bienDang(m)
        self.ganVaoLabelXuLy(res)

    #miền không gian
    def blur(self, n):
        self.blur_val.setText(str(n * 2 - 1))
        size = int(self.blur_val.text())
        res = self.ip.blur(size)
        self.ganVaoLabelXuLy(res)

    def gaussian(self, n):
        self.gaussian_val.setText(str(n * 2 - 1))
        size = int(self.gaussian_val.text())
        res = self.ip.gaussian(size)
        self.ganVaoLabelXuLy(res)

    def median(self, n):
        self.median_val.setText(str(n*2-1))
        size = int(self.median_val.text())
        res = self.ip.median(size)
        self.ganVaoLabelXuLy(res)

    def bilateral(self, sigma):
        self.bila_val.setText(str(sigma))
        size = int(self.bila_val.text())
        res = self.ip.bilateral(sigma)
        self.ganVaoLabelXuLy(res)

    def highPass(self):
        res=self.ip.highPassGaussian()
        self.ganVaoLabelXuLy(res)

    def canny(self):
        res=self.ip.canny()
        self.ganVaoLabelXuLy(res)

    #cạnh
    def sobelX(self):
        res = self.ip.sobelX()
        self.ganVaoLabelXuLy(res)
    def sobelY(self):
        res = self.ip.sobelY()
        self.ganVaoLabelXuLy(res)
    def laplacian(self):
        res = self.ip.laplacian()
        self.ganVaoLabelXuLy(res)

    #hoạt hình
    def hoatHinh(self):
        res=self.ip.hoatHinh()
        self.ganVaoLabelXuLy(res)

    #kích hoạt tool
    def mucXamTool(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()
            
            actNegative = QAction(QIcon(), 'Negative', self)
            actNegative.triggered.connect(self.negative)

            actHistogram = QAction(QIcon(), 'Histogram', self)
            actHistogram.triggered.connect(self.histogram)

            actAdaptHistogram = QAction(QIcon(), 'Adaptive Histogram', self)
            actAdaptHistogram.triggered.connect(self.adaptHistogram)

            self.toolbar.clear()
            self.toolbar.addAction(actNegative)
            self.toolbar.addAction(actHistogram)
            self.toolbar.addAction(actAdaptHistogram)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def tanSoTool(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actHighPass = QAction('High-Pass Filter', self)
            actHighPass.triggered.connect(self.highPass)
            self.toolbar.addAction(actHighPass)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def xacDinhCanhTool(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actSobelX = QAction(QIcon(), 'SobelX', self)
            actSobelX.triggered.connect(self.sobelX)
            self.toolbar.addAction(actSobelX)

            actSobelY = QAction(QIcon(), 'SobelY', self)
            actSobelY.triggered.connect(self.sobelY)
            self.toolbar.addAction(actSobelY)

            actLaplacian = QAction(QIcon(), 'Laplacian', self)
            actLaplacian.triggered.connect(self.laplacian)
            self.toolbar.addAction(actLaplacian)

            actCanny = QAction(QIcon(), 'Canny', self)
            actCanny.triggered.connect(self.canny)
            self.toolbar.addAction(actCanny)
        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

    def hoatHinhTool(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actHoatHinh = QAction(QIcon(), 'Hoạt hình hóa', self)
            actHoatHinh.triggered.connect(self.hoatHinh)
            self.toolbar.addAction(actHoatHinh)

        else:
            QMessageBox.about(self, "Thông báo", "Chọn: File -> Open image")

if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    win = Ui_MainWindow()
    sys.exit(a.exec_())

