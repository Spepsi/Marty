from Marty.utils.config.config import Config
from Marty.infrastructure.scraping.scraping import enrich_catalog

import pandas as pd
import os

config = Config()

catalog_file = config["DATA"]["CATALOG"]

catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")

enriched_catalog = enrich_catalog(catalog_file)

enriched_catalog_file = os.path.join(config["DATA"]["MAIN"], "catalog", "enriched_catalog.csv")
enriched_catalog.to_csv(enriched_catalog_file, index=False, sep=";", encoding="utf-8")
