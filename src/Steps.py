from EdgeDetectorFactory import EdgeDetectorFactory
import os
import time
from ImageUtil import ImageUtil
import numpy as np
from PIL import Image
from Susan import Susan

############################## CONFIGURE ME #############################
#########################################################################
FilterSIGMA = 1.6                                                       #
FilterDIM = 3*FilterSIGMA                                               #
                                                                        #
directory = 'Steps_Images/'                                             #
result_dir = 'Steps_Result/'                                            #
SINGLE_FASE = ["RobertsCross", "Sobel", "Prewitt"]                      #
MULTI_FASE = { "Canny": ["RobertsCross", "Sobel", "Prewitt"] }          #
ZERO_CROSS = ["MarrHildreth"]                                           #
                                                                        #
single_threshold = 100                                                  #    
double_threshold = [0.05, 0.25]                                         #
zeroCrossing_threshold = 2                                              #
#########################################################################






############## DO NOT EDIT FROM THIS POINT ##############
def load(filename):
    image = ImageUtil.loadImage( directory+filename)
    filename, extension = os.path.splitext(filename)
    return image, filename, extension

def main():
    

    edgeDetectorFactorySingle = EdgeDetectorFactory("SINGLE_FASE")
    edgeDetectorFactoryMulti = EdgeDetectorFactory("MULTI_FASE")
    edgeDetectorFactoryZero = EdgeDetectorFactory("ZERO_CROSS")
    
    edgeDetectorsSingle = []
    for detector in SINGLE_FASE:
        edgeDetectorsSingle.append(edgeDetectorFactorySingle.getDetector(detector, threshold = single_threshold))
        
    edgeDetectorsMulti = []
    for detector in MULTI_FASE.keys():
        for mask in MULTI_FASE[detector]:
            edgeDetectorsMulti.append(edgeDetectorFactoryMulti.getDetector(mask = [detector, mask], threshold = double_threshold))
    
    edgeDetectorsZero = []
    for detector in ZERO_CROSS:
        edgeDetectorsZero.append(edgeDetectorFactoryZero.getDetector(mask = [detector, ImageUtil.getLaplacianOfGaussian(FilterDIM, FilterSIGMA)], threshold = zeroCrossing_threshold))
    
    for filename in os.listdir(directory):
        if os.path.isdir(directory+filename): 
            continue
        image, filename, extension = load(filename)
        original = ImageUtil.writeInfo(image, "Original")
        blurring_time = time.time()
        image_blurred = ImageUtil.applyGaussianBlurring(image, FilterDIM, FilterSIGMA)
        blurring_time = time.time() - blurring_time
        blurred = ImageUtil.writeInfo(image_blurred, "Gaussian Blurring (Sigma: {} - Filter: {}x{})".format(FilterSIGMA,np.ceil(FilterDIM),np.ceil(FilterDIM)), blurring_time)
        for detector in edgeDetectorsSingle:
            images = []
            images_blurred = []
            #without blurring
            #gradient
            gradient_time = time.time()
            gradient = detector.getGradient(image)
            gradient_time = time.time() - gradient_time
            images.append(ImageUtil.writeInfo(gradient, "Gradient", gradient_time))
            #Threshold
            threshold_time = time.time()
            threshold = detector.applyThreshold(gradient)
            threshold_time = time.time() - threshold_time
            images.append(ImageUtil.writeInfo(threshold, "Threshold: {}".format(detector.getThreshold()), gradient_time + threshold_time))
            
            #with blurring
            #gradient
            gradient_time = time.time()
            gradient_blurred = detector.getGradient(image_blurred)
            gradient_time = time.time() - gradient_time
            images_blurred.append(ImageUtil.writeInfo(gradient_blurred, "Gradient", gradient_time + blurring_time))
            #Threshold
            threshold_time = time.time()
            threshold_blurred = detector.applyThreshold(gradient_blurred)
            threshold_time = time.time() - threshold_time
            images_blurred.append(ImageUtil.writeInfo(threshold_blurred, "Threshold: {}".format(detector.getThreshold()), gradient_time + threshold_time + blurring_time))
            
            #write output image with all information
            ImageUtil.saveSteps(original, images, blurred, images_blurred, result_dir+filename+"_"+detector.getName()+extension, detector.getName() )

        for detector in edgeDetectorsZero:
            images = []
            images_blurred = []
            #log
            log_time = time.time()
            log = detector.getLog(image)
            log_time = time.time() - log_time
            images.append(ImageUtil.writeInfo(log, "LoG", log_time))
            #zeroCrossing
            zeroc_time = time.time()
            zeroCrossing = detector.zeroCrossing(log)
            zeroc_time = time.time() - zeroc_time
            images.append(ImageUtil.writeInfo(zeroCrossing, "ZeroCrossing (TH: {})".format(detector.getThreshold()),log_time + zeroc_time))
            #write output image with all information
            ImageUtil.saveSteps(original, images, blurred, images_blurred, result_dir+filename+"_"+detector.getName()+extension, detector.getName())        

        for detector in edgeDetectorsMulti:
            images = []
            images_blurred = []
            
            #without blurring
            #Gradient
            gradient_time = time.time()
            gradient, theta = detector.getGradient(image)
            gradient_time = time.time() - gradient_time
            images.append(ImageUtil.writeInfo(gradient, "Gradient", gradient_time))
            #NonMaximumSuppression
            nms_time = time.time()
            nms = detector.nonMaxSuppression(gradient, theta)
            nms_time = time.time() - nms_time
            images.append(ImageUtil.writeInfo(nms, "Non-Maximum Suppression", gradient_time + nms_time))
            #Threshold
            threshold_time = time.time()
            threshold = detector.doubleThreshold(nms)
            threshold_time = time.time() - threshold_time
            images.append(ImageUtil.writeInfo(threshold, "Double Threshold: {:.5f} - {:.5f}".format(detector.getThreshold()[0], detector.getThreshold()[1]), gradient_time + nms_time + threshold_time))
            #Hysteresis
            hysteresis_time = time.time()
            hysteresis = detector.hysteresis(threshold)
            hysteresis_time = time.time() - hysteresis_time
            images.append(ImageUtil.writeInfo(hysteresis, "Hysteresis", gradient_time + nms_time + threshold_time + hysteresis_time))
                    
            #with blurring
            #gradient
            gradient_time = time.time()
            gradient_blurred, theta_blurred = detector.getGradient(image_blurred)
            gradient_time = time.time() - gradient_time
            images_blurred.append(ImageUtil.writeInfo(gradient_blurred, "Gradient", gradient_time))
            #NonMaximumSuppression
            nms_time = time.time()
            nms_blurred = detector.nonMaxSuppression(gradient_blurred, theta_blurred)
            nms_time = time.time() - nms_time
            images_blurred.append(ImageUtil.writeInfo(nms_blurred, "Non-Maximum Suppression", gradient_time + nms_time + blurring_time))
            #Threshold
            threshold_time = time.time()
            threshold_blurred = detector.doubleThreshold(nms_blurred)
            threshold_time = time.time() - threshold_time
            images_blurred.append(ImageUtil.writeInfo(threshold_blurred, "Double Threshold: {} - {}".format(detector.getThreshold()[0], detector.getThreshold()[1]), gradient_time + nms_time + threshold_time + blurring_time))
            #Hysteresis
            hysteresis_time = time.time()
            hysteresis_blurred = detector.hysteresis(threshold_blurred)
            hysteresis_time = time.time() - hysteresis_time
            images_blurred.append(ImageUtil.writeInfo(hysteresis_blurred, "Hysteresis", gradient_time + nms_time + threshold_time + hysteresis_time + blurring_time))
            
            #write output image with all information
            ImageUtil.saveSteps(original, images, blurred, images_blurred, result_dir+filename+"_"+detector.getName()+extension, detector.getName() )      

if __name__ == '__main__':
    main()