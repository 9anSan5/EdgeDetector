from abc import ABC
from EdgeDetector import EdgeDetector
from scipy import ndimage
from scipy import misc
import numpy as np

class MultiFaseEdgeDetector(EdgeDetector, ABC):
        
    def getGradient(self, image):        
        vertical = ndimage.convolve( image, self.mask_v )
        horizontal = ndimage.convolve( image, self.mask_h )
        G = np.hypot(horizontal, vertical)
        G = G / G.max() * 255
        theta = np.arctan2(vertical, horizontal)
        return G, theta
    
    def nonMaxSuppression(self, image, theta):
        M, N = image.shape
        Z = np.zeros((M,N), dtype=np.int32)
        angle = theta * 180. / np.pi
        angle[angle < 0] += 180

        for i in range(1,M-1):
            for j in range(1,N-1):
                q = 255
                r = 255

                #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = image[i, j+1]
                    r = image[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = image[i+1, j-1]
                    r = image[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = image[i+1, j]
                    r = image[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = image[i-1, j-1]
                    r = image[i+1, j+1]

                if (image[i,j] >= q) and (image[i,j] >= r):
                    Z[i,j] = image[i,j]
                else:
                    Z[i,j] = 0

        return Z
    
    def doubleThreshold(self, image):
        self.highThreshold = image.max() * self.highThresholdRatio
        self.lowThreshold = self.highThreshold * self.lowThresholdRatio
        M, N = image.shape
        res = np.zeros((M,N), dtype=np.int32)

        weak = np.int32(self.weak_pixel)
        strong = np.int32(self.strong_pixel)

        strong_i, strong_j = np.where(image >= self.highThreshold)
        zeros_i, zeros_j = np.where(image < self.lowThreshold)

        weak_i, weak_j = np.where((image <= self.highThreshold) & (image >= self.lowThreshold))

        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak
        res[zeros_i, zeros_j] = 0

        return (res)
    
    def hysteresis(self, image):
        M, N = image.shape  
        weak = self.weak_pixel
        strong = self.strong_pixel
        for i in range(1, M-1):
            for j in range(1, N-1):
                if (image[i,j] == weak):
                    if ((image[i+1, j-1] == strong) or (image[i+1, j] == strong) or (image[i+1, j+1] == strong)
                        or (image[i, j-1] == strong) or (image[i, j+1] == strong)
                        or (image[i-1, j-1] == strong) or (image[i-1, j] == strong) or (image[i-1, j+1] == strong)):
                        image[i, j] = strong
                    else:
                        image[i, j] = 0
        return image
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
