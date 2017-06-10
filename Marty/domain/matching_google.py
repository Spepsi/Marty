from Marty.infrastructure.google_api import GoogleVisionApi
from Marty.utils.config.config import Config

import os
import pandas as pd

config = Config()


image_from_pic = "/Users/nicolas/Projects/Marty/data/test_data/close.jpg"
image_from_pic_far = "/Users/nicolas/Projects/Marty/data/test_data/far.jpg"

api_from_pic = GoogleVisionApi(config, image_from_pic)
api_from_pic_far = GoogleVisionApi(config, image_from_pic_far)

url = api_from_pic_far.get_partial_matching_urls()[0][0]
api_from_url = GoogleVisionApi(config, url)

labels_url = api_from_url.get_labels()
labels_pic = api_from_url.get_labels()
labels_far = api_from_pic_far.get_labels()

catalog_file = "/Users/nicolas/Projects/Marty/data/catalog/catalog.csv"
catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")

class GoogleApiMatcher():
    def __init__(self, config):
        self.config = config
        data_dir = config["DATA"]["MAIN"]
        catalog_file = os.path.join(data_dir, "catalog", "catalog.csv")
        self.catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")

    def find_perfect_match(self, image_source):
        api = GoogleVisionApi(self.config, image_source)
        partial_matching_urls_with_score = api.get_partial_matching_urls()
        partial_matching_urls = [partial_url[0] for partial_url in partial_matching_urls_with_score]

        index = None
        for url in partial_matching_urls:
            catalog_filtered = self.catalog[self.catalog["URL"] == url]
            #if len(catalog_filtered) == 0:
                #print("No matching found for {}".format(url))
            if len(catalog_filtered) == 1:
                index = catalog_filtered.index
                print("yeah!")
                break
            #else:
                #print("More than one match found")

        return index
