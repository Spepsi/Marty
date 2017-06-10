import os

from Marty.domain.crop.image import Image
from Marty.domain.image_similarity.perceptual_hashing.phash import PHash



def which_image(path):
    cropped_image = Image(path).crop()
    filename = os.path.basename(path)
    root_name = filename.split(".")[1]
    SUFFIX = "_cropped.jpg"
    cropped_name = root_name + SUFFIX
    cv2.imwrite(cropped_name, cropped_image)
    closest_image = PHash(cropped_name).closest_from_database()
    return closest_image
