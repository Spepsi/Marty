from Marty.infrastructure.google_api import GoogleVisionApi
from Marty.utils.config.config import Config

import os
import pandas as pd



class GoogleApiMatcher():
    def __init__(self, config):
        self.config = config
        data_dir = config["DATA"]["MAIN"]
        catalog_file = os.path.join(data_dir, "catalog", "enriched_catalog.csv")
        self.catalog = pd.read_csv(catalog_file, sep=";", encoding="utf-8")

    def find_perfect_match(self, image_source):
        api = GoogleVisionApi(self.config, image_source)
        partial_matching_urls_with_score = api.get_partial_matching_urls()
        partial_matching_urls = [partial_url[0] for partial_url in partial_matching_urls_with_score]


        def crop_url(url):
            url_crop = "www.wga.hu" + url.split("www.wga.hu")[1]
            return url_crop

        catalog = self.catalog
        catalog["crop_URL_image_art"] = catalog["URL_image_art"].apply(crop_url)

        index = None
        for url in partial_matching_urls:
            try:
                crop_url = crop_url(url)
            except IndexError:
                continue
            url = url.replace("preview", "art")
            url = url.replace("detail", "art")
            catalog_filtered = self.catalog[self.catalog["crop_URL_image_art"] == crop_url]

            if len(catalog_filtered) == 1:
                index = catalog_filtered.index
                print("yeah!")
                break

        if index is None:
            print("No match found")
            matching_url = None
        else:
            matching_url = self.catalog.loc[index[0], "URL"]
        return matching_url


config = Config()
image_from_pic_far = "/Users/nicolas/Projects/Marty/data/test_data/far.jpg"
matcher = GoogleApiMatcher(config)
index_matching = matcher.find_perfect_match(image_from_pic_far)



catalog_file = "/Users/nicolas/Projects/Marty/data/catalog/catalog.csv"
catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")

print(catalog.loc[index_matching, "URL"])

image_842 = "/Users/nicolas/Projects/Marty/data/test_data2/842_close.jpg"
api = GoogleVisionApi(config, image_842)
urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config)
match_842 = matcher.find_perfect_match(image_842)
# KO

image = "/Users/nicolas/Projects/Marty/data/test_data2/894_close.jpg"
api = GoogleVisionApi(config, image)
urls = api.get_full_matching_urls()
partial_urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config)
match = matcher.find_perfect_match(image)
# KO

image = "/Users/nicolas/Projects/Marty/data/test_data2/898_close.jpg"
api = GoogleVisionApi(config, image)
urls = api.get_full_matching_urls()
partial_urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config)
match = matcher.find_perfect_match(image)
# KO

image = "/Users/nicolas/Projects/Marty/data/test_data2/1059_close.jpg"
api = GoogleVisionApi(config, image)
urls = api.get_full_matching_urls()
partial_urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config)
match = matcher.find_perfect_match(image)
# KO

image = "/Users/nicolas/Projects/Marty/data/test_data2/1047_close.jpg"
api = GoogleVisionApi(config, image)
urls = api.get_full_matching_urls()
partial_urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config)
match = matcher.find_perfect_match(image)
#
