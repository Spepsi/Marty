import ipdb
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
import time
from PIL import Image
import pandas as pd
from Marty.utils.config.config import Config
from Marty.application.which_image import which_image
import json


#id de la photo la plus proche ==> id dans le catalog
# 2259 ==> ARCIMBOLDO Giuseppe, Spring  faut faire un -2
def convert_url_to_image(url):
    image_url = url.replace(".html", ".jpg")
    image_url = image_url.replace("html", "detail")
    return image_url

def id_to_index(idx):
    idx = int(idx.split(".")[0])
    return idx-2

# Import similarity image
config = Config(file='config.ini')
catalog = config['DATA']['CATALOG']

recommandations = config['DATA']['RECO']
reco = pd.read_csv(recommandations, sep=",")
df = pd.read_csv(catalog, encoding="cp1250", sep=";")
df['SRC'] = df['URL'].apply(convert_url_to_image)
df.columns = [c.lower() for c in df.columns]


app = Flask(__name__)
CORS(app, resources=r'/api/*')


@app.route('/api/hello', methods=['OPTION', 'POST'])
def hello():
    print('Received request')
    img = Image.open(request.files['file0'])
    this_time = time.time()
    saved_image = '../../data/test_data2/quelquechose'+str(this_time)+'.jpg'
    img.save(saved_image)
    image_id = which_image(saved_image)
    index = id_to_index(image_id)
    image_metadata = df.iloc[index]
    as_json_tableau = image_metadata.to_json()
    
    # Add a recommandation, index 14 dans csv = 12 dans le catalogue
    reco_index = reco[reco['index_x'] == int(image_id.split(".")[0])]
    reco_index = reco_index.sort_values(by='score', ascending=False)
    reco_index = (reco_index['index_y']-2).tolist()
    recos = [df.iloc[int(i)] for i in reco_index]
    as_json_recos = [i.to_json() for i in recos]

    print(image_metadata)
    print(recos)

    return jsonify({'tableau': as_json_tableau,
                    'reco': as_json_recos})



#192.168.43.205
app.run(host='0.0.0.0')
