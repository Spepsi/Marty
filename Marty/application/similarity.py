import os
import sys
from Marty.domain.image_similarity.perceptual_hashing.phash import PHash
from Marty.utils.config.config import Config

if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = Config(CONFIG)[SECTION]["media"]



    image1 = os.path.join(MEDIA, "967.jpg")
    image2 = os.path.join(MEDIA, "968.jpg")
    image3 = os.path.join(MEDIA, "969.jpg")
    
    distance = PHash(image1).distance_to(image2)
    print("should be small: ", distance)

    distance = PHash(image1).distance_to(image3)
    print("should be high: ", distance)


    
    image1 = os.path.join(MEDIA, "982.jpg")
    image2 = os.path.join(MEDIA, "981.jpg")
    distance = PHash(image1).distance_to(image2)
    print("should be small: ", distance)

    

