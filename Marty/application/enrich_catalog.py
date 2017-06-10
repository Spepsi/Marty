from Marty.utils.config.config import Config 
from Marty.infrastructure.scraping.scraping import enrich_catalog

config = Config()

catalog_file = config["DATA"]["CATALOG"]

catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")

enriched_catalog = enrich_catalog(catalog_file)
