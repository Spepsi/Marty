from Marty.infrastructure.google_api import GoogleVisionApi
from Marty.utils.config.config import Config
from Marty.infrastructure.loader.loader import JSONLabels, JSONUrls, JSONSafeSearch, LabelsComparator

import os
import pandas as pd



class GoogleApiMatcher():
    def __init__(self, config, image_source):
        self.config = config
        data_dir = config["DATA"]["MAIN"]
        catalog_file = os.path.join(data_dir, "catalog", "enriched_catalog.csv")
        self.catalog = pd.read_csv(catalog_file, sep=";", encoding="utf-8")
        self.image_source = image_source
        self.api = GoogleVisionApi(self.config, image_source)
        self.partial_matching_urls_with_score = api.get_partial_matching_urls()


    def find_perfect_match(self):

        partial_matching_urls = [partial_url[0] for partial_url in self.partial_matching_urls_with_score]

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
            crop_url = crop_url.replace("preview", "art")
            crop_url = crop_url.replace("detail", "art")
            catalog_filtered = self.catalog[self.catalog["crop_URL_image_art"] == crop_url]

            if len(catalog_filtered) == 1:
                index = catalog_filtered.index
                print("yeah!", self.catalog.loc[index[0], :])
                break

        if index is None:
            print("No match found")
            matching_url = None
        else:
            matching_url = self.catalog.loc[index[0], "URL"]
        return matching_url

    def find_labels_match(self):
        partial_matching_urls = [partial_url[0] for partial_url in self.partial_matching_urls_with_score]
        url = partial_matching_urls[0]

        api_second = GoogleVisionApi(self.config, url)
        labels_second = api_second.get_labels()
        # Check we have a match in database
        labels_comparator = LabelsComparator(labels_second)
        database = os.listdir(config['DATA']['JSON'])
        database = [int(i.split('.')[0]) for i in database]

        match = None
        for idx in database: # Refactor after ..

            try:
                json_labels = JSONLabels(config)
                labels_to_compare = json_labels.load(idx)
                res =  labels_comparator(labels_to_compare)
                if res==True:
                    print(" It is idx : "+idx)
                    match = idx
                    break
            except:
                print("OULALA")

        return match



config = Config()
catalog_file = "/Users/nicolas/Projects/Marty/data/catalog/catalog.csv"
catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")







image = "/Users/nicolas/Projects/Marty/data/test_data2/2468_close.jpg"
api = GoogleVisionApi(config, image)
urls = api.get_full_matching_urls()
partial_urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config, image)
match = matcher.find_perfect_match()
labels_match = matcher.find_labels_match()
# OK

image = "/Users/nicolas/Projects/Marty/data/test_data2/1047_close.jpg"
api = GoogleVisionApi(config, image)
urls = api.get_full_matching_urls()
partial_urls = api.get_partial_matching_urls()
matcher = GoogleApiMatcher(config)
match = matcher.find_perfect_match(image)
#
