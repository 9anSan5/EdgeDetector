import numpy as np
from SinglePhaseEdgeDetector import SinglePhaseEdgeDetector

class Sobel(SinglePhaseEdgeDetector):

    def __init__(self, threshold = 80):
        self.threshold = threshold
        self.name = "Sobel"
        self.mask_h = np.array( [[ -1, 0, 1 ],
                                 [ -2, 0, 2 ],
                                 [ -1, 0, 1]], np.float32 )
        self.mask_v = np.array( [[ 1, 2, 1 ],
                                 [ 0, 0, 0 ],
                                 [ -1, -2, -1]], np.float32 )

