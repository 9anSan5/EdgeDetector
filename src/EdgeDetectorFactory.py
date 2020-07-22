from RobertsCross import RobertsCross
from Sobel import Sobel
from Prewitt import Prewitt
from Canny import Canny
from MarrHildret import MarrHildret


class EdgeDetectorFactory:
    def __init__(self, type):
        self.type = type
    
    def get_detector(self, mask, threshold = None):
        if self.type == "SINGLE_FASE":
            if threshold is not None:
                return self.get_single(mask, threshold)
            else:
                return self.get_single(mask)
        elif self.type == "MULTI_FASE":
            if threshold is not None:
                return self.get_multi(mask[0], mask[1], threshold[0], threshold[1])
            else:
                return self.get_multi(mask[0], mask[1])
        elif self.type == "ZERO_CROSS":
            return self.get_zero(mask[0], mask[1], threshold)
            
            
    def get_single(self, mask, threshold = 80):
        if mask == "RobertsCross":
            return RobertsCross(threshold)
        elif mask == "Sobel":
            return Sobel(threshold)
        elif mask == "Prewitt":
            return Prewitt(threshold)

    def get_multi(self, type, mask, lowThreshold = 0.05, highThreshold = 0.15):
        if type == "Canny":
            return Canny(self.get_single(mask), lowThreshold, highThreshold )
    
    def get_zero(self, type, mask, threshold):
        if type == "MarrHildret":
            return MarrHildret(mask, threshold)
