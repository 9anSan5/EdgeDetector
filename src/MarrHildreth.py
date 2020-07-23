from ZeroCrossingEdgeDetector import ZeroCrossingEdgeDetector
class MarrHildreth (ZeroCrossingEdgeDetector):
    
    def __init__(self, filter, thresholdRatio = 0.85):
        
        self.logFilter = filter
        self.name = "MarrHildreth (LoG)"
        self.thresholdRatio = thresholdRatio