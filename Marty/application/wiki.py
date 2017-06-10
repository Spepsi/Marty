import sys
import pandas as pd
import json
from  Marty.infrastructure.wiki.wiki import request_painting, request_author
from Marty.utils.config.config import Config


def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return {frame.values[0][0] : ""}
        return {i : {} for i in frame.values.squeeze().tolist()}
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.ix[:,1:]) for k,g in grouped}
    return d

config = Config(file='../../config.ini')
catalog = config['DATA']['CATALOG']
dump = config['DATA']['WIKI']
df = pd.read_csv(catalog, sep=";", encoding="CP1250")
df = df[df['FORM'] == "painting"]
df = df[['TITLE', 'AUTHOR']]
# Pour chaque tableau on récupère la page wiki associée
dict_ = recur_dictify(df[['AUTHOR', 'TITLE']])

# Parcours chaque tableau et requete :
for idx, row in df.iterrows():
    print(idx)
    author = row['AUTHOR']
    title = row['TITLE']
    if 'description' not in dict_[author]:
        try:
            req_author = request_author(author=author)
            dict_[author]['wiki'] = {
                "summary": req_author.summary,
                "title": req_author.title
            }
        except Exception as e:
            print(e)
            print("No match for author : "+str(author))
    try:
        req_painting = request_painting(author=author, title=title)
        dict_[author][title] = {
            "title": req_painting.title,
            "summary": req_painting.summary
        }
    except Exception as e:
        print(e)
        print('No match for painting '+str(title)+' from : '+str(author))
        dict_[author][title] = {
            "title": '',
            "summary": ''
        }

# dumping database
try:
    with open(dump, 'w') as f_:
        f_.write(json.dumps(dict_, sort_keys=True, indent=4))
except:
    from pdb import set_trace; set_trace()
