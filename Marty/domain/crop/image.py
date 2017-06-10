import ipdb
import math
import numpy as np
import cv2





class Image(object):
    BLURRING_KERNEL_SIZE = (15, 15)
    ELLIPSE_SIZE = (10, 10)
        
    def __init__(self, path, resize=0.5):
        self.path = path
        self.raw = cv2.imread(path)
        self.raw = self._resize(resize) 
        
    
    def crop(self):
        contours = self._estimate_contours()
        bounding_box = self._find_best_bounding_box(contours)
        return bounding_box
    

    def _estimate_contours(self):
        image = self._dilate()
        _, contours, _ = cv2.findContours(image,
                                          cv2.RETR_LIST,
                                          cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def _find_best_bounding_box(self, contours):
        """Returns the coordinate of the best bounding box (xmin, ymax, xmax, ymin).
        
        Note
        ----
        It's very confusing, in the documentation http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, they say the two first values are top left corners. This is true if you use cv2.imshow. However, in their imaging renderer, the y-axis is inverted (0 is at the top). So, in order to be matplotlib compatible, I renamed it instead bottom_left corner
        """
        contours = self._exclude_large(contours)
        best_box = [-1,-1,-1,-1] #initialize
        
        for c in contours:
            xmin, ymin, width, height = cv2.boundingRect(c)
            
            if best_box[0] < 0:
                best_box=[xmin, ymin, xmin+width, ymin+height]
            else:
                if xmin < best_box[0]:
                    best_box[0] = xmin
                if ymin < best_box[1]:
                    best_box[1] = ymin
                if xmin+width > best_box[2]:
                    best_box[2] = xmin + width
                if ymin+height > best_box[3]:
                    best_box[3] = ymin + height

        return best_box

    def _dilate(self):
        cls = self.__class__
        gray = cv2.cvtColor(self.raw, cv2.COLOR_BGR2GRAY)
        smoothed = cv2.blur(gray, cls.BLURRING_KERNEL_SIZE)
        mean_luminosity = np.average(smoothed)
        mean_luminosity = math.floor(mean_luminosity)
        _, binary = cv2.threshold(smoothed,
                                  mean_luminosity,
                                  255,
                                  cv2.THRESH_BINARY_INV)

        DILATATION_KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                                      cls.ELLIPSE_SIZE)
        dilated = cv2.morphologyEx(binary,
                                   cv2.MORPH_OPEN, #erode then dilate
                                   DILATATION_KERNEL)
        return dilated


    def _exclude_large(self, contours):
        selected_contours = []
        _MAX_IMAGE_SIZE = self.image_size
        for c in contours:
            is_smaller_than_image = cv2.contourArea(c) < _MAX_IMAGE_SIZE
            if is_smaller_than_image:
                selected_contours.append(c)

        return selected_contours

    @property
    def image_size(self):
        height, width, channels = self.raw.shape
        return height * width

    def _resize(self, resize):
        height, width, channels = self.raw.shape
        new_width = math.floor(resize * width)
        new_height = math.floor(resize * height)
        resized_image = cv2.resize(self.raw, (new_width, new_height)) 
        return resized_image
