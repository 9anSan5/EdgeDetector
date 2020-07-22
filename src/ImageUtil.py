import sys
import numpy as np
from scipy import ndimage
import scipy.io
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import math
import matplotlib.image as mpimg


class ImageUtil():

    #LOADING IMAGES
    @staticmethod
    def rgb2gray(rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

        #return gray

    @staticmethod
    def load_image(infilename) :
        img = mpimg.imread( infilename )
        if len(img.shape) > 2:
            return ImageUtil.rgb2gray(img)
        else:
            return img
    #########################################################################
    
    #GAUSSIAN FILTER
    @staticmethod
    def apply_gaussian_blurring(image, size, sigma=1):    
        return ndimage.convolve(image, ImageUtil.get_gaussian(size, sigma))

    @staticmethod
    def get_gaussian(size, sigma):
        size = int(size)
        if size%2 == 0:
            size += 1
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * np.pi * sigma**2)
        g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
        return g
    #########################################################################
    
    #LAPLACIAN OF GAUSSIAN FILTER
    @staticmethod
    def get_laplacianOfGaussian(size, sigma):
        size = int(size)
        if size%2 == 0:
            size += 1
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = - 1 / (4.0 * np.pi * sigma**4)
        g = (1-((x**2+y**2)/(2*sigma**2)))*normal
        g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * g
        return g

    @staticmethod
    def apply_log(image, size, sigma=1):    
        return ndimage.convolve(image, ImageUtil.get_laplacianOfGaussian(size, sigma))

    #########################################################################

    #CONCAT IMAGES
    @staticmethod
    def concat_h(img1, img2):
        dst = Image.new('L', (img1.width + img2.width, img1.height), color="white")
        dst.paste(img1, (0, 0))
        dst.paste(img2, (img1.width, 0))
        return dst
    
    @staticmethod
    def concat_v(img1, img2):
        dst = Image.new('L', (img1.width, img1.height + img2.height), color="white")
        dst.paste(img1, (0, 0))
        dst.paste(img2, (0, img1.height))
        return dst
    #########################################################################

    #OUTPUT GENERATOR
    @staticmethod
    def create_steps( original, edges, blurred, edges_blurred, outfilename, algorithm = None ):
        for img in edges:
            original = ImageUtil.concat_h(original,img)
        if len(edges_blurred) > 0:
            for img in edges_blurred:
                blurred = ImageUtil.concat_h(blurred,img)
            img = ImageUtil.concat_v(original, blurred)
        else:
            img = original
        if algorithm is not None:
            img = ImageUtil.add_title(img, algorithm)    
        img.save(outfilename)

    @staticmethod
    def create_all( original, edges, groundTruth, results, outfilename) :
        for img in edges:
            original = ImageUtil.concat_h(original,img)
        for img in results:
            groundTruth = ImageUtil.concat_h(groundTruth,img)
        img = ImageUtil.concat_v(original, groundTruth)
        img.save(outfilename)
    #########################################################################
    

    #WRITE TEXT
    @staticmethod
    def write_info(image, string, time = None):
        if not type(image.size) == tuple:
            image = Image.fromarray(image)
        width, height = image.size
        img = Image.new('L', (width, 60), color='white')
        draw = ImageDraw.Draw(img)
        info1 = string
        font = ImageFont.truetype("arial.ttf", 16)
        w1, h1 = draw.textsize(info1, font)
        if time is not None:
            info2 = "Time: {:.5f} sec".format(time)
            w2, h2 = draw.textsize(info2, font) 
            draw.text(((img.width-w1)/2,(((img.height-h1)/2))-h1/2), info1, font = font)
            draw.text(((img.width-w2)/2,((img.height-h2)/2)+h1/2), info2, font = font)
        else:
            draw.text(((img.width-w1)/2,((img.height-h1)/2)), info1, font = font)
        dst = Image.new('L', (width, height+img.height))
        dst.paste(img, (0, 0))
        dst.paste(image, (0, img.height))
        return dst
        
    @staticmethod
    def add_title(image, title):
        img = Image.new('L', (image.size[0], 60), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        w, h = draw.textsize(title, font)
        draw.text(((img.width-w)/2,((img.height-h)/2)), title, font = font)
        dst = Image.new('L', (image.width, image.height+img.height))
        dst.paste(img, (0, 0))
        dst.paste(image, (0, img.height))
        return dst

    @staticmethod
    def create_result(shape, tp, fp, tn, fn, mq, mae, pfom):
        img = Image.new('L', (shape[0], shape[1]), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 24)
        tp = "TP: {}".format(tp)
        fp = "FP: {}".format(fp)
        tn = "TN: {}".format(tn)
        fn = "FN: {}".format(fn)
        mq = "MQ: {:.4f}".format(mq)
        mae = "MAE: {:.4f}".format(mae)
        pfom = "Pratt FOM: {:.4f}".format(pfom) 
        w1, h1 = draw.textsize(tp, font)
        w2, h2 = draw.textsize(fp, font)
        w3, h3 = draw.textsize(tn, font)
        w4, h4 = draw.textsize(fn, font)
        w5, h5 = draw.textsize(mq, font)
        w6, h6 = draw.textsize(mae, font)
        w7, h7 = draw.textsize(pfom, font)
        draw.text(((img.width-w1)/2,((img.height-h1)/2)-h1-h2-h3-h4-h5-h6), tp, font = font)
        draw.text(((img.width-w2)/2,((img.height-h2)/2)+h1-h2-h3-h4-h5-h6), fp, font = font)
        draw.text(((img.width-w3)/2,((img.height-h3)/2)+h1+h2-h3-h4-h5-h6), tn, font = font)
        draw.text(((img.width-w4)/2,((img.height-h4)/2)+h1+h2+h3-h4-h5-h6), fn, font = font)
        draw.text(((img.width-w5)/2,((img.height-h5)/2)+h1+h2+h3+h4-h5-h6), mq, font = font)
        draw.text(((img.width-w6)/2,((img.height-h6)/2)+h1+h2+h3+h4+h5-h6), mae, font = font)
        draw.text(((img.width-w7)/2,((img.height-h7)/2)+h1+h2+h3+h4+h5+h6), pfom, font = font)
        return img
    #########################################################################