from PIL import Image
import imagehash


class PHash(object):
    def __init__(self, image):
        self.image = image

    def distance_to(self, image2):
        hash1 = imagehash.average_hash(Image.open(self.image))
        hash2 = imagehash.average_hash(Image.open(image2))
        return hash1 - hash2
         
