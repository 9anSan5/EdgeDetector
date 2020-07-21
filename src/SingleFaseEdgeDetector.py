from abc import ABC, abstractmethod
from scipy import ndimage
from scipy import misc
import numpy as np
from PIL import Image

class SingleFaseEdgeDetector(ABC):    
        
    def get_gradient(self, image):
        vertical = ndimage.convolve( image, self.mask_v )
        horizontal = ndimage.convolve( image, self.mask_h )
        
        G = np.hypot(horizontal, vertical)
        G = G / G.max() * 255
        return G 
    
    def apply_threshold(self, img):
        M, N = img.shape
        img[img > self.threshold] = 255
        img[img <= self.threshold] = 0
        return img
        
    def getMask(self):
        return self.mask_h, self.mask_v
    
    def getName(self):
        return self.name
    
    def getThreshold(self):
        return self.threshold
    
    def getEdges(self, image):
        gradient = self.get_gradient(image)
        threshold = self.apply_threshold(gradient)
        return threshold