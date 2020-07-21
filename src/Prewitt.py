import numpy as np
from SingleFaseEdgeDetector import SingleFaseEdgeDetector

class Prewitt(SingleFaseEdgeDetector):

    def __init__(self, threshold = 80):
        self.threshold = threshold
        self.name = "Prewitt"
        self.mask_h = np.array( [[ 1, 0, -1 ],
                                 [ 1, 0, -1 ],
                                 [ 1, 0, -1]], np.float32 )
        self.mask_v = np.array( [[ 1, 1, 1 ],
                                 [ 0, 0, 0 ],
                                 [ -1, -1, -1]], np.float32 )

