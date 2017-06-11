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

# Import similarity image
config = Config(file='config.ini')
catalog = config['DATA']['CATALOG']

#id de la photo la plus proche ==> id dans le catalog
# 2259 ==> ARCIMBOLDO Giuseppe, Spring  faut faire un -2

def id_to_index(idx):
    idx = int(idx.split(".")[0])
    return idx-2

df = pd.read_csv(catalog, encoding="cp1250", sep=";")


app = Flask(__name__)
CORS(app, resources=r'/api/*')


@app.route('/api/hello', methods=['OPTION', 'POST'])
def hello():
    print('ok')
    img = Image.open(request.files['file0'])
    this_time = time.time()
    saved_image = '../../data/test_data2/quelquechose'+str(this_time)+'.jpg'
    img.save(saved_image)
    image_id = which_image(saved_image)
    index = id_to_index(image_id)

    image_metadata = df.iloc[index]
    print(image_metadata)
    as_json = image_metadata.to_json()
    return jsonify(as_json)


@app.route('/api/recommandation', methods=['OPTION'])
def get_recomandation(user):
    pass
#192.168.43.205
app.run(host='0.0.0.0')
