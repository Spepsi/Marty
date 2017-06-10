import math
import os
import sys
import collections
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from Marty.utils.config.config import Config
from Marty.domain.crop.image import Image



def add_rectangle(ax, contour, edgecolor="r"):
    xmin, ymin, xmax, ymax = contour
    width = xmax - xmin
    height = ymax - ymin
    bottom_left = (xmin, ymin)

    bounding_box = patches.Rectangle(bottom_left,
                                     width,
                                     height,
                                     linewidth=3,
                                     edgecolor=edgecolor,
                                     facecolor="none")
    ax.add_patch(bounding_box)


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = Config(CONFIG)[SECTION]["media"]
    MEDIA = "/Users/ldocao/Google Drive/Documents/Professionnel/2015 10 26 Quantmetry/Externe/01 Missions/2017 06 10 Hackathon Marty/Marty/data/test_data2/"
    FILE = os.path.join(MEDIA, "898_crop2.jpg")


    image = Image(FILE, resize=1)
    raw = image.raw    
    best_contour = image.crop()

    
    #plot
    fig, ax = plt.subplots(1)
    plt.imshow(raw)
    add_rectangle(ax, best_contour, edgecolor="g")
    plt.savefig("contour.png", bbox_inches='tight')



