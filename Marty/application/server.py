from flask import Flask, request, jsonify
# from flask_restful import Resource, Api, reqparse
from flask import render_template
from flask_cors import CORS
import time
from PIL import Image
import pandas as pd

from Marty.utils.config.config import Config
import json

# Import similarity image
config = Config(file='../../config.ini')
catalog = config['DATA']['CATALOG']

#id de la photo la plus proche ==> id dans le catalog
# 2259 ==> ARCIMBOLDO Giuseppe, Spring  faut faire un -2

def id_to_index(idx):
    return idx-2

df = pd.read_csv(catalog,encoding="cp1250", sep=";")
from pdb import set_trace; set_trace()

app = Flask(__name__)
CORS(app, resources=r'/api/*')

@app.route('/api/image/', methods=['OPTION'])
def get_corresponding_image(image):
    print(1)  # ecriture sur le back

    return "23"  # valeur retourne au client


@app.route('/api/hello', methods=['OPTION', 'POST'])
def hello():
    print('ok')

    img = Image.open(request.files['file0'])
    this_time = time.time()
    img.save('../../data/test_data2/quelquechose'+str(this_time)+'.jpg')

    # Recupere une serie pandas
    # Description : TITRE, AUTEUR, ANNEE, TECHINIQUE, URL Description, recommandation ==> Array de Description
    return 'ok'


@app.route('/api/recommandation', methods=['OPTION'])
def get_recomandation(user):
    pass
#192.168.43.205
app.run(host='0.0.0.0')