import math

import cv2 as cv
import numpy as np
from scipy import ndimage

class ImageProcessing:
    def __init__(self, imgfile, w, h):
        self.imgfile = imgfile
        self.width = w
        self.height = h
        self.img = cv.imread(imgfile)
        self.img = cv.resize(self.img, (w, h))

    #chapter 2
    def scaling(self, size):
        return cv.resize(self.img, None, fx = size*0.01, fy = size*0.01, interpolation=cv.INTER_CUBIC)

    def translation(self,x,y):
        rows, cols, chs =self.img.shape
        M=np.float32([[1,0,x],[0,1,y]])
        return cv.warpAffine(self.img,M,(cols,rows))

    def rotation(self, angle):
        rows, cols, chs = self.img.shape
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), 360 - angle, 1)
        return cv.warpAffine(self.img, M, (cols, rows))

    def shearing(self, m):
        rows, cols, chs = self.img.shape
        pts1 = np.float32([[50,m],[200,50],[50,200]])
        pts2 = np.float32([[10,100],[200,50],[100,250]])
        M = cv.getAffineTransform(pts1,pts2)
        return cv.warpAffine(self.img,M,(cols,rows))

    #chapter 3
    def negative(self):
        return ~self.img

    def log(self, thresh):
        res_1 = np.uint8(np.log(self.img))
        res_2 = cv.threshold(res_1, thresh, 255, cv.THRESH_BINARY)[1]
        return res_2

    def gamma(self, gamma):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        return cv.LUT(self.img, table)

    def histogram(self):
        img_yuv = cv.cvtColor(self.img, cv.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])
        return cv.cvtColor(img_yuv, cv.COLOR_YUV2RGB)

    def adapt_histogram(self):
        # create a CLAHE object (Arguments are optional).
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_yuv = cv.cvtColor(self.img, cv.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])
        return cv.cvtColor(img_yuv, cv.COLOR_YUV2RGB)

    #chapter 4
    def blur(self, n):
        return cv.blur(self.img, (n,n))

    def gaussian(self, n):
        return cv.GaussianBlur(self.img, (n,n), 0)

    def median(self, n):
        return cv.medianBlur(self.img, n)

    def bilateral(self, sigma):
        return cv.bilateralFilter(self.img,9,sigma,sigma)

    def gauss_noise_img(self):
        gauss_n = np.random.normal(0, 40, self.img.shape)
        gauss_n_img = np.add(gauss_n, np.float32(self.img))
        return gauss_n_img

    def erlang_noise_img(self):
        erlang_n = np.random.gamma(10, 20, size=self.img.shape)
        erlang_n_img = np.add(erlang_n, np.float32(self.img))
        return erlang_n_img

    def rayleigh_noise_img(self):
        rayleigh_n = np.random.rayleigh(50, size=self.img.shape)
        rayleigh_n_img = np.add(rayleigh_n, np.float32(self.img))
        return rayleigh_n_img

    def uniform_noise_img(self):
        uniform_n = np.random.uniform(low= -50, high= 50, size=self.img.shape)
        uniform_n_img = np.add(uniform_n, np.float32(self.img))
        return uniform_n_img

    def cartoon(self):
        img_rgb = self.img
        numDownSamples = 2
        numBilateralFilters = 50

        # -- STEP 1 --
        # downsample image using Gaussian pyramid
        img_color = img_rgb
        for _ in range(numDownSamples):
            img_color = cv.pyrDown(img_color)
        
        for _ in range(numBilateralFilters):
            img_color = cv.bilateralFilter(img_color, 9, 9, 7)
        
        for _ in range(numDownSamples):
            img_color = cv.pyrUp(img_color)
        
        # -- STEPS 2 and 3 --
        # convert to grayscale and apply median blur
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
        img_blur = cv.medianBlur(img_gray, 3)
        
        # -- STEP 4 --
        # detect and enhance edges
        img_edge = cv.adaptiveThreshold(img_blur, 255,
                                         cv.ADAPTIVE_THRESH_MEAN_C,
                                         cv.THRESH_BINARY, 9, 2)
       
        # -- STEP 5 --
        # convert back to color so that it can be bit-ANDed with color image
        (x,y,z) = img_color.shape
        img_edge = cv.resize(img_edge,(y,x)) 
        img_edge = cv.cvtColor(img_edge, cv.COLOR_GRAY2RGB)
        return cv.bitwise_and(img_color, img_edge)

    #chapter 5
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
        I = cv.imread(self.imgfile,0)
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
        I = cv.imread(self.imgfile,0)
        h, w = I.shape
        H = ideal_filter_lp(h, w)
        f = np.fft.fft2(I)
        G = np.fft.fftshift(f)
        Ip = G*H
        Im = np.abs(np.fft.ifft2(np.fft.ifftshift(Ip)))
        return np.uint8(Im)

    def gaussian_hp(self):
        data = np.array(self.img, dtype=np.float32)
        lowpass = ndimage.gaussian_filter(data, 3)
        gauss_highpass = data - lowpass
        gauss_highpass = np.uint8(gauss_highpass)
        gauss_highpass = ~gauss_highpass
        return gauss_highpass
    
    #chapter 8
    def sobelX(self):
        return cv.Sobel(self.img, cv.CV_8U, 1, 0, ksize=7)

    def sobelY(self):
        return cv.Sobel(self.img, cv.CV_8U, 0, 1, ksize=5)

    def laplacian(self):
        return cv.Laplacian(self.img, cv.CV_8U)

    def canny(self):
        image = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        return cv.Canny(image, 100, 200)