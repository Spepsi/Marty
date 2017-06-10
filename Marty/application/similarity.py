import glob
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches


from Marty.domain.crop.image import Image
from Marty.utils.config.config import Config

if __name__  == "__main__":
    CONFIG = sys.argv[1]
    SECTION = "similarity"
    MEDIA = "/Users/ldocao/Google Drive/Documents/Professionnel/2015 10 26 Quantmetry/Externe/01 Missions/2017 06 10 Hackathon Marty/Marty/data/test_data2/"

    counter = 0
    os.chdir(MEDIA)
    for image in glob.glob("*.jpg"):
        original_image = Image(image, resize=1).raw
        best_contour = Image(image, resize=1)._find_best_bounding_box()
        cropped_image = Image(image).crop()


        xmin, ymin, xmax, ymax = best_contour
        width = xmax - xmin
        height = ymax - ymin
        bottom_left = (xmin, ymin)

    
        #plot
        fig, ax = plt.subplots(1)
        root_name = image.split(".")[0]
        plt.imshow(cropped_image)
        plt.savefig(root_name+"_cropped.png", bbox_inches='tight')

        fig, ax = plt.subplots(1)
        plt.imshow(original_image)
        bounding_box = patches.Rectangle(bottom_left,
                                         width,
                                         height,
                                         linewidth=3,
                                         edgecolor="g",
                                         facecolor="none")
        ax.add_patch(bounding_box)
        plt.savefig(root_name+"_original.png", bbox_inches="tight")
