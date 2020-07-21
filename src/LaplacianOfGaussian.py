from ZeroCrossingEdgeDetector import ZeroCrossingEdgeDetector
class LaplacianOfGaussian (ZeroCrossingEdgeDetector):
    
    def __init__(self, filter, thresholdRatio = 0.85):
        
        self.logFilter = filter
        self.name = "LoG"
        self.thresholdRatio = thresholdRatio