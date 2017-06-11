from Marty.infrastructure.google_api import GoogleVisionApi
from Marty.utils.config.config import Config
from Marty.infrastructure.loader.loader import JSONLabels, JSONUrls, JSONSafeSearch, LabelsComparator, JSONWebEntities, JSONColors

import os
import pandas as pd
import numpy as np
from itertools import combinations

config = Config()
catalog_file = "/Users/nicolas/Projects/Marty/data/catalog/catalog.csv"
catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")
catalog.index = catalog.index + 2
catalog = catalog[catalog["FORM"] == "painting"]
database = os.listdir(config['DATA']['JSON'])
database = [int(i.split('.')[0]) for i in database if "json" in i]
database = sorted(database)

enhanced_catalog = catalog.copy()
colors_columns = ["color_" + str(i+1) for i in range(3)]
web_entities_columns = ["web_entity_" + str(i+1) for i in range(5)]

enhanced_catalog = pd.concat([enhanced_catalog,
                                pd.DataFrame(columns=colors_columns),
                                pd.DataFrame(columns=web_entities_columns)])

enhanced_catalog.reset_index(inplace=True)

enhancing = pd.DataFrame(index = enhanced_catalog.index,
                            columns = colors_columns + web_entities_columns)

def add_colors(idx):
    try:
        idx = int(idx)
        colors = JSONColors(config).load(idx)
    except:
        colors = tuple([np.nan for _ in range(3)])
    return colors
    #return ((1,2),(3,44),(5,6))

def add_web_entities(idx):
    try:
        web_entities = JSONWebEntities(config).load(idx)
    except:
        web_entities = tuple([np.nan for _ in range(5)])
    return web_entities

enhanced_catalog["color_1"], enhanced_catalog["color_2"], enhanced_catalog["color_3"]= zip(*enhanced_catalog["index"].map(add_colors))
enhanced_catalog["web_entity_1"], enhanced_catalog["web_entity_2"], enhanced_catalog["web_entity_3"], enhanced_catalog["web_entity_4"], enhanced_catalog["web_entity_5"] = zip(*enhanced_catalog["index"].map(add_web_entities))

enhanced_catalog.to_csv(os.path.join(config["DATA"]["MAIN"], "catalog", "enhanced_catalog.csv"),
                            sep=";", encoding="utf-8")
