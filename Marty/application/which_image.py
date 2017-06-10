import os
import glob
import cv2

from Marty.domain.crop.image import Image
from Marty.domain.image_similarity.perceptual_hashing.phash import PHash



def which_image(path):
    cropped_image = Image(path).crop()
    filename = os.path.basename(path)
    root_name = filename.split(".")[0]
    SUFFIX = "_cropped.jpg"
    cropped_name = root_name + SUFFIX
    cv2.imwrite(cropped_name, cropped_image)
    closest_image = PHash(cropped_name).closest_from_database()
    return closest_image


# PHOTO_DIR = "/Users/ldocao/Google Drive/Documents/Professionnel/2015 10 26 Quantmetry/Externe/01 Missions/2017 06 10 Hackathon Marty/Marty/data/test_data2"
# photos_list = glob.glob(PHOTO_DIR+"/*.jpg")


# for photo in photos_list:
#     closest_id = which_image(photo)
#     print(photo, closest_id[0])
