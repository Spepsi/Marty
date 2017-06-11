import os
import math
import numpy as np
from matplotlib import pyplot as plt
import cv2
from Marty.domain.crop.image import Image



def generate_variation(path):
    DIRECTORY = "/Users/etiennefongue/Documents/Marty/data/test_data2/"
    original = os.path.join(DIRECTORY,path)
    rootname = path.split(".")[0]
    variation_1 = os.path.join(DIRECTORY,rootname+"_grey_1.jpg")
    variation_2 = os.path.join(DIRECTORY,rootname+"_grey_2.jpg")
    return original,variation_1,variation_2

def decompose_crop(path):
    BLURRING_KERNEL_SIZE = (300, 300)
    ELLIPSE_SIZE = (10, 10)
    

    raw = cv2.imread(path)
    gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    blurred = cv2.blur(gray, BLURRING_KERNEL_SIZE)
    mean_luminosity = np.average(blurred)
    mean_luminosity = math.floor(mean_luminosity)

    _, binary = cv2.threshold(blurred,
                              mean_luminosity,
                              255,
                              cv2.THRESH_BINARY_INV)

    DILATATION_KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                                ELLIPSE_SIZE)
    dilated = cv2.morphologyEx(binary,
                               cv2.MORPH_OPEN, #erode then dilate
                               DILATATION_KERNEL)
    
    return gray,blurred,binary,dilated

path,path1,path2 = generate_variation("2669_close.jpg")
gray,blurred,binary,dilated = decompose_crop(path)
gray1,blurred1,binary1,dilated1 = decompose_crop(path1)
gray2,blurred2,binary2,dilated2 = decompose_crop(path2)



images = [gray,blurred,binary,dilated,
            gray1,blurred1,binary1,dilated1,
            gray2,blurred2,binary2,dilated2]
for i in range(len(images)):
    
    plt.subplot(3,4,i+1)
    plt.imshow(images[i],'gray')
    #plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

"""
img = cv2.imread(path,0)
img = cv2.medianBlur(img,5)
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
#titles = ['Original Image', 'Global Thresholding (v = 127)',
#            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']


img_1 = cv2.imread(path1,0)
img_1 = cv2.medianBlur(img_1,5)
ret_1,th1_1 = cv2.threshold(img_1,127,255,cv2.THRESH_BINARY)
th2_1 = cv2.adaptiveThreshold(img_1,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3_1 = cv2.adaptiveThreshold(img_1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
#titles = ['Original Image', 'Global Thresholding (v = 127)',
#            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']


img_2 = cv2.imread(path2,0)
img_2 = cv2.medianBlur(img_2,5)
ret_2,th1_2 = cv2.threshold(img_2,127,255,cv2.THRESH_BINARY)
th2_2 = cv2.adaptiveThreshold(img_2,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3_2 = cv2.adaptiveThreshold(img_2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)




dilated=Image(path)._dilate()
dilated_1=Image(path1)._dilate()
dilated_2=Image(path2)._dilate()
#titles = ['Original Image', 'Global Thresholding (v = 127)',
#            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

images = [img, th1, th2, th3, dilated,
         img_1, th1_1, th2_1, th3_1, dilated_1,
          img_2, th1_2, th2_2, th3_2,dilated_2]
for i in range(len(images)):
    plt.subplot(3,5,i+1),plt.imshow(images[i],'gray')
    #plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
"""


