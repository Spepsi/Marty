import os
import glob
import pandas as pd
import cv2
import functools
from PIL import Image
import imagehash


from Marty.domain.crop.image import Image as ImageCropper


#@functools.lru_cache(maxsize=None, typed=False)
def get_image_hash(path):
    return imagehash.phash(Image.open(path), hash_size=16)








    
class PHash(object):
    DATABASE = "/Users/ldocao/Google Drive/Documents/Professionnel/2015 10 26 Quantmetry/Externe/01 Missions/2017 06 10 Hackathon Marty/Marty/data/pict"
    
    def __init__(self, image):
        """
        Parameters
        ----------
        image: str
            Path to file
        """
        self.image = image
        self.hash = get_image_hash(image)

        
    def closest_from_database(self, n=1):
        """
        Parameters
        ----------
        n: int
            Top N closest images found in database (default:1)
        """
        distances = self.get_distances()
        distances.sort_values("distance", ascending=True, inplace=True)
        return distances.index[0:n+1]
    
        
    def get_distances(self):
        image_list = self._find_images()
        primary_key = [i.split("/")[-1:][0] for i in image_list]
        distances = pd.DataFrame(columns=["distance"], index=primary_key)
        for i in image_list:
            index = i.split("/")[-1:][0]
            i_hash = get_image_hash(i)
            distances.loc[index]["distance"] = i_hash - self.hash

        return distances
            
    @classmethod
    def _find_images(cls):
        directory = cls.DATABASE
        regexp = "*.jpg"
        lookup = os.path.join(directory, regexp)
        image_list = glob.glob(lookup)
        return image_list
        
