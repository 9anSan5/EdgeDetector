from MultiPhaseEdgeDetector import MultiPhaseEdgeDetector
class Canny (MultiPhaseEdgeDetector):
    
    def __init__(self, operator, lowThresholdRatio, highThresholdRatio):
        
        self.mask_h, self.mask_v = operator.getMask()
        self.name = "Canny ("+operator.getName()+" Filter)"
        self.lowThresholdRatio = lowThresholdRatio
        self.highThresholdRatio = highThresholdRatio
        self.weak_pixel = 25
        self.strong_pixel = 255