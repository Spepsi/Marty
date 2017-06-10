import os
import sys
from Marty.domain.image_similarity.perceptual_hashing.phash import PHash
from Marty.utils.config.config import Config

if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = Config(CONFIG)[SECTION]["media"]


    reference = os.path.join(MEDIA, "20247.jpg")
    centered2 = os.path.join(MEDIA, "centered2.jpg")
    centred = os.path.join(MEDIA, "centred.jpg")
    far = os.path.join(MEDIA, "far.jpg")
    fromSide = os.path.join(MEDIA, "fromSide.jpg")

    print(PHash(reference).distance_to(reference))
    print(PHash(reference).distance_to(centred))
    print(PHash(centered2).distance_to(centred))
    print(PHash(reference).distance_to(fromSide))
    print(PHash(reference).distance_to(far))
    print()

