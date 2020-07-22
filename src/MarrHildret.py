from ZeroCrossingEdgeDetector import ZeroCrossingEdgeDetector
class MarrHildret (ZeroCrossingEdgeDetector):
    
    def __init__(self, filter, thresholdRatio = 0.85):
        
        self.logFilter = filter
        self.name = "MarrHildret (LoG)"
        self.thresholdRatio = thresholdRatio