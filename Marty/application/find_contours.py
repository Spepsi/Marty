import os
import sys
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from Marty.utils.config.config import Config
from Marty.domain.crop.image import Image

if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = Config(CONFIG)[SECTION]["media"]
    FILE = os.path.join(MEDIA, "992.jpg")


    image = Image(FILE, resize=1)
    raw = image.raw
    
    contours = image._estimate_contours()
    best_contour = image.crop()
    xmin, ymin, xmax, ymax = best_contour
    width = xmax - xmin
    height = ymax - ymin
    bottom_left = (xmin, ymin)

    
    #plot
    fig, ax = plt.subplots(1)
    plt.imshow(raw)
    bounding_box = patches.Rectangle(bottom_left,
                                     width,
                                     height,
                                     linewidth=3,
                                     edgecolor="g",
                                     facecolor="none")
    ax.add_patch(bounding_box)
    plt.savefig("contour.png", bbox_inches='tight')
