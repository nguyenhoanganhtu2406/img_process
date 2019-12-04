import sys
import cv2 as cv

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QFileDialog, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon

from ip import ImageProcessing as IP

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.filename = ""
        super(Ui_MainWindow, self).__init__()
        uic.loadUi("interface.ui", self)
        self.setWindowTitle("Image Processing")
        self.show()
        self.Init()
        self.ip = ""
        self.toolbar = False
        self.img_exist = False
        self.x_current = 0
        self.y_current = 0
        self.setWindowIcon(QIcon("icon/mainicon.png"))
        self.curImg = False
        QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def Init(self):
        #bắt các sự kiện action
        self.act_open_img.triggered.connect(self.open_image)
        self.act_gray.triggered.connect(self.gray_click)
        self.act_freq.triggered.connect(self.freq_click)
        self.act_edge.triggered.connect(self.edge_click)
        self.act_noise.triggered.connect(self.noise_click)
        self.act_cartoon.triggered.connect(self.cartoon_click)
        self.act_save.triggered.connect(self.save_img)

        #mapping widget to function
        #geomatric
        self.rotation_inp.valueChanged.connect(self.rotation)
        self.scaling_inp.valueChanged.connect(self.scaling)
        self.tranX_inp.valueChanged.connect(self.getTranX)
        self.tranY_inp.valueChanged.connect(self.getTranY)
        self.shear_inp.valueChanged.connect(self.shearing)

        #gray
        self.log_inp.valueChanged.connect(self.log)
        self.gamma_inp.valueChanged.connect(self.gamma)

        #spatial domain
        self.median_inp.valueChanged.connect(self.median)
        self.bila_inp.valueChanged.connect(self.bilateral)
        self.gaussian_inp.valueChanged.connect(self.gaussian)
        self.blur_inp.valueChanged.connect(self.blur)


    def save_img(self):
        img = self.curImg
        s = self.filename[0]
        print(s)
        photoName = ""
        for i in range(len(s) - 1, 0, -1):
            if s[i] == '/':
                photoName = s[i + 1:len(s) - 4]
                photoName = photoName + "_Changed" + s[len(s) - 4:]
                break

        q = QMessageBox.question(self, "Confirmation", "Save current image?", QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        if (q == QMessageBox.Yes):
            cv.imwrite(photoName, img)
            QMessageBox.about(self, "Alert", "Saved successfully")

    def open_image(self):
        self.filename = QFileDialog.getOpenFileName(self, "Choose Image", "", 
                            "Images File(*.jpg; *.jpeg; *.png, *.tif);;Python Files (*.py)")
        if(self.filename[0] != ''):
            width = self.org_label.width()
            height = self.org_label.height()
            self.org_label.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            self.pro_label.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            width = self.org_label.width()
            height = self.org_label.height()
            self.ip = IP(self.filename[0], width, height)
            self.img_exist = True
            self.geo_group_enable()
            self.spatial_group_enable()
            self.gray_group_enable()

    def geo_group_enable(self):
        if (self.img_exist == True):
            self.geo_group.setEnabled(True)
        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def spatial_group_enable(self):
        if (self.img_exist == True):
            self.spatial_group.setEnabled(True)
        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def gray_group_enable(self):
        if (self.img_exist == True):
            self.gray_group.setEnabled(True)
        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def bind_to_label(self, changed_img):
        qformat = QImage.Format_Indexed8
        self.curImg=changed_img

        if len(changed_img.shape) == 3:
            if (changed_img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(changed_img, changed_img.shape[1], changed_img.shape[0], changed_img.strides[0], qformat)
        # BGR > RGB
        img = img.rgbSwapped()
        self.pro_label.setPixmap(QPixmap.fromImage(img))
        self.pro_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    #geometric
    def negative(self):
        res = self.ip.negative()
        self.bind_to_label(res)

    def histogram(self):
        res = self.ip.histogram()
        self.bind_to_label(res)

    def adapt_histogram(self):
        res = self.ip.adapt_histogram()
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

    #gray
    def log(self, m):
        self.log_val.setText(str(m))
        res = self.ip.log(m)
        self.bind_to_label(res)

    def gamma(self, m):
        self.gamma_val.setText(str("{0:.1f}".format(round(m*0.1, 1))))
        res = self.ip.gamma(m*0.1)
        self.bind_to_label(res)

    #spatial domain
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

    #noise
    def gauss_noise(self):
        res=self.ip.gauss_noise_img()
        self.bind_to_label(res)

    def erlang_noise(self):
        res=self.ip.erlang_noise_img()
        self.bind_to_label(res)

    def rayleigh_noise(self):
        res=self.ip.rayleigh_noise_img()
        self.bind_to_label(res)

    def uniform_noise(self):
        res=self.ip.uniform_noise_img()
        self.bind_to_label(res)

    #cartoon
    def cartoon(self):
        res=self.ip.cartoon()
        self.bind_to_label(res)

    
    def gauss_hp(self):
        res=self.ip.gaussian_hp()
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

    #trigger action on toolbar
    def gray_click(self):
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
        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def freq_click(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()
                
            act_gauss_hp = QAction('High-Pass Filter', self)
            act_gauss_hp.triggered.connect(self.gauss_hp)

            self.toolbar.addAction(act_gauss_hp)
        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def edge_click(self):
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
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def cartoon_click(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            act_cartoon = QAction(QIcon(), 'Cartoon', self)
            act_cartoon.triggered.connect(self.cartoon)
            self.toolbar.addAction(act_cartoon)

        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

    def noise_click(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            act_gauss_noise = QAction(QIcon(), 'Gauss Noise', self)
            act_gauss_noise.triggered.connect(self.gauss_noise)
            self.toolbar.addAction(act_gauss_noise)

            act_erlang_noise = QAction(QIcon(), 'Erlang Noise', self)
            act_erlang_noise.triggered.connect(self.erlang_noise)
            self.toolbar.addAction(act_erlang_noise)

            act_rayleigh_noise = QAction(QIcon(), 'Rayleigh Noise', self)
            act_rayleigh_noise.triggered.connect(self.rayleigh_noise)
            self.toolbar.addAction(act_rayleigh_noise)

            act_uniform_noise = QAction(QIcon(), 'Uniform Noise', self)
            act_uniform_noise.triggered.connect(self.uniform_noise)
            self.toolbar.addAction(act_uniform_noise)

        else:
            QMessageBox.about(self, "Alert", "To enable all functions, select image first: File -> Open image")

if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    win = Ui_MainWindow()
    sys.exit(a.exec_())

