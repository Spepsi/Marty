import math
import numpy as np
import cv2





class Image(object):
    BLURRING_KERNEL_SIZE = (100, 100)
    ELLIPSE_SIZE = (10, 10)
        
    def __init__(self, path, resize=1):
        self.path = path
        self.raw = cv2.imread(path)
        self.raw = self._resize(resize) 
        
    
    def crop(self):
        bounding_box = self._find_best_bounding_box()
        cropped_image = self._crop_given(bounding_box)
        return cropped_image
    

    def _find_best_bounding_box(self):
        """Returns the coordinate of the best bounding box (xmin, ymin, xmax, ymax).
        
        Note
        ----
        It's very confusing, in the documentation http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, they say the two first values are top left corners. This is true if you use cv2.imshow. However, in their imaging renderer, the y-axis is inverted (0 is at the top). So, in order to be matplotlib compatible, I renamed it instead bottom_left corner
        """
        contours = self._estimate_contours()
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


    def _crop_given(self, bounding_box):
        xmin = bounding_box[0]
        ymin = bounding_box[1]
        xmax = bounding_box[2]
        ymax = bounding_box[3]
        cropped = self.raw[ymin:ymax, xmin:xmax, :]
        return cropped

    def _estimate_contours(self):
        image = self._dilate()
        _, contours, _ = cv2.findContours(image,
                                          cv2.RETR_LIST,
                                          cv2.CHAIN_APPROX_SIMPLE)

        return contours

    
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
