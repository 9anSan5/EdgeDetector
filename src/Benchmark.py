from EdgeDetectorFactory import EdgeDetectorFactory
import os
import time
from MetricsFunction  import MetricsFunction
from ImageUtil import ImageUtil
import numpy as np
from PIL import Image

FilterSIGMA = 2.3
FilterDIM = 3*FilterSIGMA
directory = 'Benchmark_Images/'
result_dir = 'Benchmark_Result/'
groundtruth_dir = directory+'GroundTruth/'
SINGLE_FASE = ["RobertsCross", "Sobel", "Prewitt"]
MULTI_FASE = { "Canny": ["RobertsCross", "Sobel", "Prewitt"] }
ZERO_CROSS = ["MarrHildret"]

single_threshold = 80
double_threshold = [0.1, 0.30]
zeroCrossing_threshold = 0.98

def load_image(filename):
    image = ImageUtil.load_image( directory+filename )
    filename, extension = os.path.splitext(filename)
    return image, filename, extension

def load_groundTruth(filename):
    image = ImageUtil.load_image( groundtruth_dir+filename)
    return image

def main():
    
    edgeDetectorFactorySingle = EdgeDetectorFactory("SINGLE_FASE")
    edgeDetectorFactoryMulti = EdgeDetectorFactory("MULTI_FASE")
    edgeDetectorFactoryZero = EdgeDetectorFactory("ZERO_CROSS")
    
    edgeDetectors = []
    for detector in SINGLE_FASE:
        edgeDetectors.append(edgeDetectorFactorySingle.get_detector(detector, threshold = single_threshold))
    for detector in MULTI_FASE.keys():
        for mask in MULTI_FASE[detector]:
            edgeDetectors.append(edgeDetectorFactoryMulti.get_detector(mask = [detector, mask], threshold = double_threshold))
    for detector in ZERO_CROSS:
        edgeDetectors.append(edgeDetectorFactoryZero.get_detector(mask = [detector, ImageUtil.get_laplacianOfGaussian(FilterDIM, FilterSIGMA)], threshold = zeroCrossing_threshold))

    for filename in os.listdir(directory):
        if os.path.isdir(directory+filename): 
            continue
        image, filename, extension = load_image(filename)
        groundTruth = load_groundTruth(filename+extension)
        original = ImageUtil.write_info(image, "Original")
        blurring_time = time.time()
        image = ImageUtil.apply_gaussian_blurring(image, FilterDIM, FilterSIGMA)
        blurring_time = time.time() - blurring_time
        images = []
        results = []
        groundTruth = Image.fromarray(groundTruth.astype(np.int32))
        for detector in edgeDetectors:
            
            t = time.time()
            edges = detector.getEdges(image)
            t = time.time() - t

            tp, fp, tn, fn, mq = MetricsFunction.MapQuality(groundTruth, edges)
            pfom = MetricsFunction.PrattFigureMerit(groundTruth, edges)
            mae = MetricsFunction.MeanAbsoluteError(groundTruth, edges)
            images.append(ImageUtil.write_info(edges, detector.getName()+" (TH: {})".format(detector.getThreshold()), blurring_time + t))
            
            results.append(ImageUtil.create_result(groundTruth.size, tp, fp, tn, fn, mq, mae, pfom))
            
        #write output image with all information
        ImageUtil.create_all(original, images, groundTruth, results, result_dir+filename+extension)   
if __name__ == '__main__':
    main()