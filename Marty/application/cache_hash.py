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

    hashes = pd.DataFrame(columns=["filename", "phash"])
    counter = 0
    os.chdir(MEDIA)
    for image in glob.glob("*.jpg"):
        phash = imagehash.phash(Image.open(image))
        hashes.loc[counter] = [image, phash]
        print(hashes.loc[counter])
        counter += 1

    hashes.to_csv("phash.csv", index=False)
