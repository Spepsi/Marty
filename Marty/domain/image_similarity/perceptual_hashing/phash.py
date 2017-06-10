import os
import ipdb

import cv2
import pandas as pd
import functools
from PIL import Image
import imagehash

import matplotlib.pyplot as plt
plt.style.use('classic')


from Marty.domain.crop.image import Image as ImageCropper


@functools.lru_cache(maxsize=None, typed=False)
def get_image_hash(path):
    return imagehash.average_hash(Image.open(path))

    
class PHash(object):
    def __init__(self, image):
        self.crop(image)
        self.image = "temporary.jpg"
        self.hash = get_image_hash(self.image)


    @staticmethod
    def crop(image):
        cropped = ImageCropper(image).crop()
        try:
            os.remove("temporary.jpg")
        except FileNotFoundError:
            pass
        cv2.imwrite("temporary.jpg", cropped)


        
    def closest_from(self, image_list):
        distances = self.get_distances(image_list)
        distances.sort_values("distance", ascending=True, inplace=True)
        print(distances)
        return distances.index[0]
    
        
    def get_distances(self, image_list):
        primary_key = [i.split("/")[-1:][0] for i in image_list]
        distances = pd.DataFrame(columns=["distance"], index=primary_key)
        for i in image_list:
            index = i.split("/")[-1:][0]
            i_hash = get_image_hash(i)
            distances.loc[index]["distance"] = i_hash - self.hash

        return distances
            
        
