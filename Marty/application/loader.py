from Marty.utils.config.config import  Config
from Marty.infrastructure.loader.loader import JSONLabels, JSONUrls, JSONSafeSearch, LabelsComparator
from Marty.infrastructure.google_api import GoogleVisionApi
import os
config = Config(file='../../config.ini')

labels = JSONLabels(config)
url = JSONUrls(config)
safe_search = JSONSafeSearch(config)

image_source = os.path.join(config['DATA']['TEST'], "898_crop3.jpg")
vision = GoogleVisionApi(config, image_source=image_source)
labels = vision.get_labels()
url = vision.get_full_matching_urls()
# Do we have a full match ?
# Suppose No ... get partial match
# Suppose not, then we do a query on first partial matching
partials = vision.get_partial_matching_urls()
vision_second = GoogleVisionApi(config, image_source=partials[0][0])
# get labels
labels_second = vision_second.get_labels()
# Check we have a match in database
labels_comparator = LabelsComparator(labels_second)
database = os.listdir(config['DATA']['JSON'])
database = [int(i.split('.')[0]) for i in database]
for idx in database: # Refactor after ..
    labels_to_compare = JSONLabels(config, idx)
    res =  labels_comparator(labels_to_compare)
    if res==True:
        print(" It is idx : "+idx)
        break
# Comparer avec toute la base
# Création de la base de données de mots ?

# Dans le cas ou google api ne renvoie pas exactement les url
# On relance une requête de mot sur l'url donné et on compare les résultats avec notre base

