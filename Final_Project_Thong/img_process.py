import math
import cv2 as cv
import numpy as np
from scipy import ndimage

class ImageProcessing:
    def __init__(self, file_img, w, h):
        self.file_img = file_img
        self.width = w
        self.height = h
        self.img = cv.imread(file_img)
        self.img = cv.resize(self.img, (w, h))

    def tiLe(self, size):
        return cv.resize(self.img, dsize=None, fx=size*0.01, fy=size*0.01, interpolation=cv.INTER_CUBIC)

    def tinhTien(self,x,y):
        rows, cols, chs =self.img.shape
        M=np.float32([[1,0,x],[0,1,y]])
        return cv.warpAffine(self.img,M,(cols,rows))

    def gocQuay(self, goc):
        rows, cols, chs = self.img.shape
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), 360 - goc, 1)
        return cv.warpAffine(self.img, M, (cols, rows))

    def bienDang(self, m):
        rows, cols, chs = self.img.shape
        pts1 = np.float32([[50,m],[200,50],[50,200]])
        pts2 = np.float32([[10,100],[200,50],[100,250]])
        M = cv.getAffineTransform(pts1,pts2)
        return cv.warpAffine(self.img,M,(cols,rows))

    def negative(self):
        res = ~self.img
        return res

    def histogram(self):
        img_yuv = cv.cvtColor(self.img, cv.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])
        res = cv.cvtColor(img_yuv, cv.COLOR_YUV2RGB)
        return res

    def log(self, thresh):
        res_1 = np.uint8(np.log(self.img))
        res_2 = cv.threshold(res_1, thresh, 255, cv.THRESH_BINARY)[1]
        return res_2

    def gamma(self, gamma):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        res = cv.LUT(self.img, table)
        return res

    def adaptHistogram(self):
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_yuv = cv.cvtColor(self.img, cv.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])
        res = cv.cvtColor(img_yuv, cv.COLOR_YUV2RGB)
        return res

    def blur(self, n):
        res = cv.blur(self.img, (n,n))
        return res

    def gaussian(self, n):
        res = cv.GaussianBlur(self.img, (n,n), 0)
        return res

    def median(self, n):
        res = cv.medianBlur(self.img, n)
        return res

    def hoatHinh(self):
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 5)
        edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)

        color = cv.bilateralFilter(self.img, 9, 300, 300)

        cartoon = cv.bitwise_and(color, color, mask=edges)
        return cartoon

    def bilateral(self, sigma):
        return cv.bilateralFilter(self.img,9,sigma,sigma)

    def butterworth_filter_lp(self, sx, sy, d0=40, n=1):
        hr = sx/2
        hc = sy/2
        x = np.arange(-hc, hc)
        y = np.arange(-hr, hr)

        [x, y] = np.meshgrid(x, y)
        mg = np.sqrt(x**2 + y**2)
        return 1/(1+(mg/d0)**(2*n))

    def butterworth_filter_hp(self, sx, sy, d0=40, n=1):
        return 1 - self.butterworth_filter_lp(sx, sy, d0, n)

    def butterworth_lp(self):
        I = cv.imread(self.file_img,0)
        h, w = I.shape
        H = butterworth_filter_lp(h, w)
        f = np.fft.fft2(I)
        G = np.fft.fftshift(f)
        Ip = G*H
        Im = np.abs(np.fft.ifft2(np.fft.ifftshift(Ip)))
        return np.uint8(Im)

    def ideal_filter_lp(self, sx, sy, d0=40):
        hr = sx/2
        hc = sy/2
        x = np.arange(-hc, hc)
        y = np.arange(-hr, hr)

        [x,y] = np.meshgrid(x, y)
        mg = np.sqrt(x**2 + y**2)
        return np.float32(mg <= d0)

    def ideal_filter_hp(self, sx, sy, d0=40):
        return 1 - self.ideal_filter_lp(sx, sy, d0)

    def ideal_lp(self):
        I = cv.imread(self.file_img,0)
        h, w = I.shape
        H = ideal_filter_lp(h, w)
        f = np.fft.fft2(I)
        G = np.fft.fftshift(f)
        Ip = G*H
        Im = np.abs(np.fft.ifft2(np.fft.ifftshift(Ip)))
        return np.uint8(Im)

    def highPassGaussian(self):
        data = np.array(self.img, dtype=np.float32)
        lowpass = ndimage.gaussian_filter(data, 3)
        gauss_highpass = data - lowpass
        gauss_highpass = np.uint8(gauss_highpass)
        gauss_highpass = ~gauss_highpass
        return gauss_highpass
    
    def sobelX(self):
        return cv.Sobel(self.img, cv.CV_8U, 1, 0, ksize=7)

    def sobelY(self):
        return cv.Sobel(self.img, cv.CV_8U, 0, 1, ksize=5)

    def laplacian(self):
        return cv.Laplacian(self.img, cv.CV_8U)

    def canny(self):
        image = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        return cv.Canny(image, 100, 200)