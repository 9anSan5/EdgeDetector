from abc import ABC
from EdgeDetector import EdgeDetector
from scipy import ndimage
import numpy as np

class ZeroCrossingEdgeDetector(EdgeDetector, ABC):

    def getLog(self, image):
        G = ndimage.convolve(image, self.logFilter)
        G = G / G.max() * 255  
        return G

    def zeroCrossing(self, LoG):
        self.threshold = np.mean(np.abs(LoG)) * self.thresholdRatio
        zero_crossing = np.zeros_like(LoG)
        for i in range(1,LoG.shape[0]-1):
            for j in range(1,LoG.shape[1]-1):
                patch = LoG[i-1:i+2, j-1:j+2]
                maxP = patch.max()
                minP = patch.min()
                if LoG[i][j] == 0:
                    if (LoG[i][j-1] < 0 and LoG[i][j+1] > 0) or (LoG[i][j-1] < 0 and LoG[i][j+1] < 0) or (LoG[i-1][j] < 0 and LoG[i+1][j] > 0) or (LoG[i-1][j] > 0 and LoG[i+1][j] < 0):
                        if ((maxP - minP) > self.threshold):
                            zero_crossing[i][j] = 255
                        else:
                            zero_crossing[i][j] = 0
                if LoG[i][j] < 0:
                    if (LoG[i][j-1] > 0) or (LoG[i][j+1] > 0) or (LoG[i-1][j] > 0) or (LoG[i+1][j] > 0):
                        if ((maxP - minP) > self.threshold):
                            zero_crossing[i][j] = 255
                        else:
                            zero_crossing[i][j] = 0

        return zero_crossing

    def getMask(self):
        return self.getMask

    def getName(self):
        return self.name

    def getThreshold(self):
        return float('%.4f'%self.threshold)


    def getEdges(self, image):
        log = self.getLog(image)
        z = self.zeroCrossing(log)
        return z