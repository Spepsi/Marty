import sys
import pandas as pd

from  Marty.infrastructure.wiki.wiki import request_painting
from Marty.utils.config.config import Config

config = Config(file='../../config.ini')
catalog = config['DATA']['CATALOG']
df = pd.read_csv(catalog, sep=";", encoding="CP1250")

df = df[['TITLE', 'AUTHOR']]

author = df['AUTHOR'].iloc[0]
title = df['TITLE'].iloc[0]

res = request_painting(author, title)
from pdb import set_trace; set_trace()
