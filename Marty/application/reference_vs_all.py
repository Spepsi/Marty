import os
import sys
import glob

import pandas as pd

from PIL import Image
import imagehash

from Marty.utils.config.config import Config


if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = Config(CONFIG)[SECTION]["media"]

    hashes = pd.DataFrame(columns=["filename", "distance"])
    counter = 0
    os.chdir(MEDIA)
    for image in glob.glob("*.jpg"):
        reference = imagehash.phash(Image.open("20247.jpg"))
        phash = imagehash.phash(Image.open(image))
        hashes.loc[counter] = [image, reference - phash]
        counter += 1

    hashes.set_index("filename", inplace=True)
    hashes.sort_values("distance", inplace=True)
    hashes.loc["far.jpg"]
    hashes.loc["fromSide.jpg"]
