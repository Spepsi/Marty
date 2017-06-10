from Marty.infrastructure.google_api import GoogleVisionApi
from Marty.utils.config.config import Config

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
