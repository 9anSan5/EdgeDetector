from RobertsCross import RobertsCross
from Sobel import Sobel
from Prewitt import Prewitt
from Canny import Canny
from MarrHildret import MarrHildret


class EdgeDetectorFactory:
    def __init__(self, type):
        self.type = type
    
    def getDetector(self, mask, threshold = None):
        if self.type == "SINGLE_FASE":
            if threshold is not None:
                return self.getSingle(mask, threshold)
            else:
                return self.getSingle(mask)
        elif self.type == "MULTI_FASE":
            if threshold is not None:
                return self.getMulti(mask[0], mask[1], threshold[0], threshold[1])
            else:
                return self.getMulti(mask[0], mask[1])
        elif self.type == "ZERO_CROSS":
            return self.getZero(mask[0], mask[1], threshold)
            
            
    def getSingle(self, mask, threshold = 80):
        if mask == "RobertsCross":
            return RobertsCross(threshold)
        elif mask == "Sobel":
            return Sobel(threshold)
        elif mask == "Prewitt":
            return Prewitt(threshold)

    def getMulti(self, type, mask, lowThreshold = 0.05, highThreshold = 0.15):
        if type == "Canny":
            return Canny(self.getSingle(mask), lowThreshold, highThreshold )
    
    def getZero(self, type, mask, threshold):
        if type == "MarrHildret":
            return MarrHildret(mask, threshold)
