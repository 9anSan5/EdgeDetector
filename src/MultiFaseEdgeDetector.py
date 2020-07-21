from abc import ABC
from EdgeDetector import EdgeDetector
from scipy import ndimage
from scipy import misc
import numpy as np

class MultiFaseEdgeDetector(EdgeDetector, ABC):
        
    def get_gradient(self, image):        
        vertical = ndimage.convolve( image, self.mask_v )
        horizontal = ndimage.convolve( image, self.mask_h )
        G = np.hypot(horizontal, vertical)
        G = G / G.max() * 255
        theta = np.arctan2(vertical, horizontal)
        return G, theta
    
    def nonMaxSuppression(self, img, D):
        M, N = img.shape
        Z = np.zeros((M,N), dtype=np.int32)
        angle = D * 180. / np.pi
        angle[angle < 0] += 180

        for i in range(1,M-1):
            for j in range(1,N-1):
                try:
                    q = 255
                    r = 255

                   #angle 0
                    if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                    #angle 45
                    elif (22.5 <= angle[i,j] < 67.5):
                        q = img[i+1, j-1]
                        r = img[i-1, j+1]
                    #angle 90
                    elif (67.5 <= angle[i,j] < 112.5):
                        q = img[i+1, j]
                        r = img[i-1, j]
                    #angle 135
                    elif (112.5 <= angle[i,j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]

                    if (img[i,j] >= q) and (img[i,j] >= r):
                        Z[i,j] = img[i,j]
                    else:
                        Z[i,j] = 0


                except IndexError as e:
                    pass

        return Z
    
    def double_threshold(self, img):
        self.highThreshold = img.max() * self.highThresholdRatio
        self.lowThreshold = self.highThreshold * self.lowThresholdRatio
        M, N = img.shape
        res = np.zeros((M,N), dtype=np.int32)

        weak = np.int32(self.weak_pixel)
        strong = np.int32(self.strong_pixel)

        strong_i, strong_j = np.where(img >= self.highThreshold)
        zeros_i, zeros_j = np.where(img < self.lowThreshold)

        weak_i, weak_j = np.where((img <= self.highThreshold) & (img >= self.lowThreshold))

        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak

        return (res)
    
    def hysteresis(self, img):
        M, N = img.shape  
        weak = self.weak_pixel
        strong = self.strong_pixel
        for i in range(1, M-1):
            for j in range(1, N-1):
                if (img[i,j] == weak):
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
        return img
    def getMask(self):
        return self.mask_h, self.mask_v
    
    def getName(self):
        return self.name

    def getThreshold(self):
        return float('%.4f'%self.lowThreshold), float('%.4f'%self.highThreshold)
    
    def getEdges(self, image):
        gradient, theta = self.get_gradient(image)
        nms = self.nonMaxSuppression(gradient, theta)
        threshold = self.double_threshold(nms)
        hysteresis = self.hysteresis(threshold)
        return hysteresis
