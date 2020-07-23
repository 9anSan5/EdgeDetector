from EdgeDetectorFactory import EdgeDetectorFactory
import os
import time
from MetricsFunction  import MetricsFunction
from ImageUtil import ImageUtil
import numpy as np
from PIL import Image

############################## CONFIGURE ME #############################
#########################################################################
FilterSIGMA = 2.3                                                       #
FilterDIM = 3*FilterSIGMA                                               #
                                                                        #
directory = 'Benchmark_Images/'                                         #
result_dir = 'Benchmark_Result/'                                        #
groundtruth_dir = directory+"GroundTruth/"                              #
SINGLE_FASE = ["RobertsCross", "Sobel", "Prewitt"]                      #
MULTI_FASE = { "Canny": ["RobertsCross", "Sobel", "Prewitt"] }          #
ZERO_CROSS = ["MarrHildreth"]                                           #
                                                                        #
single_threshold = 80                                                   #    
double_threshold = [0.10, 0.30]                                         #
zeroCrossing_threshold = 2                                              #
#########################################################################






############## DO NOT EDIT FROM THIS POINT ##############
def loadImage(filename):
    image = ImageUtil.loadImage( directory+filename )
    filename, extension = os.path.splitext(filename)
    return image, filename, extension

def loadGroundTruth(filename):
    image = ImageUtil.loadImage( groundtruth_dir+filename)
    return image

def main():
    
    edgeDetectorFactorySingle = EdgeDetectorFactory("SINGLE_FASE")
    edgeDetectorFactoryMulti = EdgeDetectorFactory("MULTI_FASE")
    edgeDetectorFactoryZero = EdgeDetectorFactory("ZERO_CROSS")
    
    edgeDetectors = []
    for detector in SINGLE_FASE:
        edgeDetectors.append(edgeDetectorFactorySingle.getDetector(detector, threshold = single_threshold))
    for detector in MULTI_FASE.keys():
        for mask in MULTI_FASE[detector]:
            edgeDetectors.append(edgeDetectorFactoryMulti.getDetector(mask = [detector, mask], threshold = double_threshold))
    for detector in ZERO_CROSS:
        edgeDetectors.append(edgeDetectorFactoryZero.getDetector(mask = [detector, ImageUtil.getLaplacianOfGaussian(FilterDIM, FilterSIGMA)], threshold = zeroCrossing_threshold))

    for filename in os.listdir(directory):
        if os.path.isdir(directory+filename): 
            continue
        image, filename, extension = loadImage(filename)
        groundTruth = loadGroundTruth(filename+extension)
        original = ImageUtil.writeInfo(image, "Original")
        blurring_time = time.time()
        image_blurred = ImageUtil.applyGaussianBlurring(image, FilterDIM, FilterSIGMA)
        blurring_time = time.time() - blurring_time
        images = []
        results = []
        groundTruth = Image.fromarray(groundTruth).convert('1')
        for detector in edgeDetectors:
            if detector.getName() == "MarrHildret (LoG)":
                t = time.time()
                edges = detector.getEdges(image)
                t = time.time() - t
            else:
                t = time.time()
                edges = detector.getEdges(image_blurred)
                t = time.time() - t

            tp, fp, tn, fn, mq = MetricsFunction.mapQuality(groundTruth, edges)
            pfom = MetricsFunction.prattFigureMerit(groundTruth, edges)
            mae = MetricsFunction.meanAbsoluteError(groundTruth, edges)
            images.append(ImageUtil.writeInfo(edges, detector.getName()+" (TH: {})".format(detector.getThreshold()), blurring_time + t))
            
            results.append(ImageUtil.writeResult(groundTruth.size, tp, fp, tn, fn, mq, mae, pfom))
            
        #write output image with all information
        ImageUtil.saveBenchmark(original, images, groundTruth, results, result_dir+filename+extension)   
if __name__ == '__main__':
    main()