from google.cloud import vision
from Marty.utils.config.config import Config

class GoogleVisionApi():
    PROJECT = "Marty"

    def __init__(self, config, image_source):
        self.API_KEY = config["API"]["GOOGLE"]
        self.json_client = config["API"]["JSON"]
        #self.client = vision.Client.(project=self.__class__.PROJECT)
        self.client = vision.Client.from_service_account_json(
            self.json_client)
        # TODO : Mettre dans fichier de config
        self.load_image(image_source)

    def load_image(self, image_source):
        image_source_type = self._infer_image_type(image_source)
        #import pdb;pdb.set_trace()
        if image_source_type == "url":
            self.load_image_from_url(image_source)
        elif image_source_type == "local_file":
            self.load_image_from_local(image_source)

    def load_image_from_local(self, image_source):
        with open(image_source, 'rb') as imread:
            content = imread.read()
            image = self.client.image(
                content=content)
            self.image = image

    def load_image_from_url(self, image_source):
            image = self.client.image(source_uri=image_source)
            self.image = image

    @staticmethod
    def _infer_image_type(image_source):
        """Infer if the image source is an url or local file
        """
        http_in_image_file = "http" in image_source
        if http_in_image_file:
            image_source_type = 'url'
        else:
            image_source_type = "local_file"
        return image_source_type

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
