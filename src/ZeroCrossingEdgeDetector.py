from abc import ABC
from EdgeDetector import EdgeDetector
from scipy import ndimage
import numpy as np

class ZeroCrossingEdgeDetector(EdgeDetector, ABC):

    def getLog(self, image):
        G = ndimage.convolve(image, self.logFilter)
        G = G / G.max() * 255  
        return G

    def zeroCrossing(self, log):
        self.threshold = np.mean(np.abs(log)) * self.thresholdRatio
        zero_crossing = np.zeros_like(log)
        for i in range(1,log.shape[0]-1):
            for j in range(1,log.shape[1]-1):
                patch = log[i-1:i+2, j-1:j+2]
                maxP = patch.max()
                minP = patch.min()
                if log[i][j] == 0:
                    if (log[i][j-1] < 0 and log[i][j+1] > 0) or (log[i][j-1] < 0 and log[i][j+1] < 0) or (log[i-1][j] < 0 and log[i+1][j] > 0) or (log[i-1][j] > 0 and log[i+1][j] < 0):
                        if ((maxP - minP) > self.threshold):
                            zero_crossing[i][j] = 255
                        else:
                            zero_crossing[i][j] = 0
                if log[i][j] < 0:
                    if (log[i][j-1] > 0) or (log[i][j+1] > 0) or (log[i-1][j] > 0) or (log[i+1][j] > 0):
                        if ((maxP - minP) > self.threshold):
                            zero_crossing[i][j] = 255
                        else:
                            zero_crossing[i][j] = 0

        return zero_crossing

        """
    def zeroCrossing(self, LoG):
        self.threshold = np.mean(np.abs(LoG)) * self.thresholdRatio
        output = np.zeros(LoG.shape)
        w = output.shape[1]
        h = output.shape[0]

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                patch = LoG[y-1:y+2, x-1:x+2]
                p = LoG[y, x]
                maxP = patch.max()
                minP = patch.min()
                if (p > 0):
                    zeroCross = True if minP < 0 else False
                else:
                    zeroCross = True if maxP > 0 else False
                if ((maxP - minP) > self.threshold) and zeroCross:
                    output[y, x] = 1
        output = output/output.max()*255
        output = np.uint8(output)
        return output
"""
    def getName(self):
        return self.name

    def getThreshold(self):
        return float('%.4f'%self.threshold)


    def getEdges(self, image):
        log = self.getLog(image)
        z = self.zeroCrossing(log)
        return z