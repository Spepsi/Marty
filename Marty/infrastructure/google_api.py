from google.cloud import vision
from Marty.utils.config.config import Config


class GoogleVisionApi():
    PROJECT = "martyarty"

    def __init__(self, config, image_file):
        self.API_KEY = config["API"]["GOOGLE"]
        self.client = vision.Client(project=self.__class__.PROJECT)
        self.load_image(image_file)


    def load_image(self, image_file):
        with open(image_file, 'rb') as imread:
            content = imread.read()
            image = vision_client.image(
                content=content)
            self.image = image

    def get_labels(self):
        labels = self.image.detect_labels()
        labels = [(label.description, label.score) for label in labels]
        return labels

    def get_full_matching_urls(self):
        web = self.image.detect_web()
        full_matching_images = web.full_matching_images
        full_matching_urls = [full_matching_image.url for full_matching_image in full_matching_images]
        return full_matching_urls

    def get_partial_matching_urls(self):
        web = self.image.detect_web()
        partial_matching_images = web.partial_matching_images
        partial_matching_urls = [(partial_matching_image.url,partial_matching_image.score)
                                    for partial_matching_image in partial_matching_images]
        return partial_matching_urls

config = Config()
image = "/Users/nicolas/Projects/Marty/dataToTest/centred.jpg"

if False:
    config = Config()

    API_KEY = config["API"]["GOOGLE"]

    # Instantiates a client
    vision_client = vision.Client(project='Marty', credentials=API_KEY)

    # The name of the image file to annotate
    file_name = "chat.jpeg"

    # Loads the image into memory
    with open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content)

    # Performs label detection on the image file
    labels = image.detect_labels()

    print('Labels:')
    for label in labels:
        print(label.description)
