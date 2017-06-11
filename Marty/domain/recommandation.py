from Marty.infrastructure.google_api import GoogleVisionApi
from Marty.utils.config.config import Config
from Marty.infrastructure.loader.loader import JSONLabels, JSONUrls, JSONSafeSearch, LabelsComparator

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

catalog["index"] = catalog.index

#catalog.reset_index(inplace=True)
df_final = pd.DataFrame(columns = list(catalog.columns) + ["label", "prob"])
for idx in database: # Refactor after ..
    try:
        line = catalog.loc[idx].values
        json_labels = JSONLabels(config)
        labels = json_labels.load(idx)
        df = pd.DataFrame([line for _ in range(len(labels))], columns = catalog.columns)
        df["label"] = [label[0] for label in labels]
        df["prob"] = [label[1] for label in labels]
        df_final = pd.concat([df_final, df])
    except:
        pass

def score(s):
    n_words_in_commun = len(s)
    total = s.mean()
    result = (1-total)
    result *= n_words_in_commun
    return result

to_drop = ["painting", "art", "modern art", "person"]


df_final = df_final[~df_final["label"].isin(to_drop)]

df_final = df_final.merge(df_final[["index","label", "prob"]], on="label")
df_final["score"] = np.abs(df_final["prob_x"] - df_final["prob_y"])

similarities = df_final.groupby(["index_x", "index_y"])["score"].apply(score).reset_index()

similarities["same_index"] = similarities.apply(lambda row: True if row["index_x"] == row["index_y"] else False, axis=1)
similarities = similarities[similarities["same_index"] == False].drop(["same_index"], axis=1)
similarities = similarities[similarities["score"] != np.inf]
s = similarities.sort_values(by="score", ascending=False)

similarities.to_csv(os.path.join(config["DATA"]["RECOMMANDATIONS"], "recos.csv"), index=False)
