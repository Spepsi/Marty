import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches


from Marty.domain.crop.image import Image
from Marty.utils.config.config import Config

if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = Config(CONFIG)[SECTION]["media"]
    FILE = os.path.join(MEDIA, "far.jpg")

    original_image = Image(FILE, resize=1).raw
    best_contour = Image(FILE, resize=1)._find_best_bounding_box()
    cropped_image = Image(FILE).crop()


    xmin, ymin, xmax, ymax = best_contour
    width = xmax - xmin
    height = ymax - ymin
    bottom_left = (xmin, ymin)

    
    #plot
    fig, ax = plt.subplots(1)
    plt.imshow(cropped_image)
    plt.savefig("cropped.png", bbox_inches='tight')

    fig, ax = plt.subplots(1)
    plt.imshow(original_image)
    bounding_box = patches.Rectangle(bottom_left,
                                     width,
                                     height,
                                     linewidth=3,
                                     edgecolor="g",
                                     facecolor="none")
    ax.add_patch(bounding_box)

    plt.savefig("original.png", bbox_inches="tight")
