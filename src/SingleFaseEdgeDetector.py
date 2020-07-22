from abc import ABC, abstractmethod
from scipy import ndimage
from scipy import misc
import numpy as np
from PIL import Image

class SingleFaseEdgeDetector(ABC):    
        
    def getGradient(self, image):
        vertical = ndimage.convolve( image, self.mask_v )
        horizontal = ndimage.convolve( image, self.mask_h )
        
        G = np.hypot(horizontal, vertical)
        G = G / G.max() * 255
        return G 
    
    def applyThreshold(self, image):
        image[image > self.threshold] = 255
        image[image <= self.threshold] = 0
        return image
        
    def getMask(self):
        return self.mask_h, self.mask_v
    
    def getName(self):
        return self.name
    
    def getThreshold(self):
        return self.threshold
    
    def getEdges(self, image):
        gradient = self.getGradient(image)
        threshold = self.applyThreshold(gradient)
        return threshold