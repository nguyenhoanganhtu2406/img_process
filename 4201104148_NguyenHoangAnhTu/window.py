# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import cv2 as cv
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi("first_window.ui", self)

        self.image = None
        self.processedImage = None
        self.setupAction()
        self.show()

    def label_text(self, text):
        return '<html><head/><body><p><span style=" font-size:12pt; font-weight:600;">'\
            +text+'</span></p></body></html>'

    def setupAction(self):
        self.actionOpen.triggered.connect(self.openFile)
        self.btn_blur.clicked.connect(self.blur_img)
        self.btn_gauss.clicked.connect(self.gauss_blur_img)
        self.btn_med.clicked.connect(self.med_blur_img)
        self.btn_bila.clicked.connect(self.bila_filter_img)
        self.btn_composite_laplacian.clicked.connect(self.unsharp_mask)
        #btn_composite_laplacian

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.img_before.setText(_translate("MainWindow", "TextLabel"))
        self.img_after.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def openFile(self):
        self.filename,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Open...", QtCore.QDir.currentPath())
        self.image = QtGui.QImage(self.filename)
        self.imgPixmap = QtGui.QPixmap.fromImage(self.image)
        self.img_before.setPixmap(self.imgPixmap)

    def blur_img(self):
        self.matrix_img = cv.imread(self.filename)
        self.matrix_img = cv.blur(self.matrix_img, ksize=(5,5))
        # arr = np.array([[1,1,1], [1,1,1], [1,1,1]], np.float)
        # kernel = np.multiply(1/9, arr)
        # self.matrix_img = cv.filter2D(self.matrix_img, -1, kernel)
        self.label_after.setText(self.label_text("Averaging Image"))
        self.show_img()

    def gauss_blur_img(self):
        self.matrix_img = cv.imread(self.filename)
        self.matrix_img = cv.GaussianBlur(self.matrix_img, ksize=(5,5), sigmaX=0)
        self.label_after.setText(self.label_text("Gaussian Blurring Image"))
        self.show_img()

    def med_blur_img(self):
        self.matrix_img = cv.imread(self.filename)
        self.matrix_img = cv.medianBlur(self.matrix_img, ksize=5)
        self.label_after.setText(self.label_text("Median Blurring Image"))
        self.show_img()

    def bila_filter_img(self):
        self.matrix_img = cv.imread(self.filename)
        self.matrix_img = cv.bilateralFilter(self.matrix_img,d=9,sigmaColor=75,sigmaSpace=75)
        self.label_after.setText(self.label_text("Bilateral Filtering Image"))
        self.show_img()

    def laplacian_img(self):
        self.matrix_img = cv.imread(self.filename)
        kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype= np.float)
        # kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype= np.float)
        laplacian_matrix_img = cv.filter2D(self.matrix_img, -1, kernel)
        self.matrix_img = self.matrix_img - laplacian_matrix_img
        self.label_after.setText(self.label_text("Laplacian Image"))
        self.show_img()

    def composite_laplacian_img(self):
        self.matrix_img = cv.imread(self.filename)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype= np.float32)
        composite_laplacian_matrix_img = cv.filter2D(self.matrix_img, -1, kernel)
        self.matrix_img = composite_laplacian_matrix_img
        self.label_after.setText(self.label_text("Composite Laplacian Image"))
        self.show_img()

    def high_boost(self):
        self.matrix_img = cv.imread(self.filename)
        blur_img = cv.blur(self.matrix_img, ksize=(3,3))
        self.matrix_img = 3*self.matrix_img - 2*blur_img
        self.label_after.setText(self.label_text("high_boost"))
        self.show_img()

    def unsharp_mask(self):
        self.matrix_img = cv.imread(self.filename)
        al = 0.7
        kernel = np.array([[-al, al-1, -al], [al-1, al+5, al-1], [-al, al-1, -al]], dtype= np.float32)
        # kernel = kernel/(al+1)
        kernel = np.multiply(1/(al+1), kernel)
        self.matrix_img = cv.filter2D(self.matrix_img, -1, kernel)
        self.label_after.setText(self.label_text("unsharp_mask"))
        self.show_img()

    def direct_filter(self, parameter_list):
        # cv.rand
        pass

    def show_img(self):
        img = QtGui.QImage(self.matrix_img, self.matrix_img.shape[1], self.matrix_img.shape[0], 
                            self.matrix_img.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
        pix = QtGui.QPixmap(img)
        self.img_after.setPixmap(pix)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    app.exec_()
