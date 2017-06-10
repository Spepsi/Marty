import json
import os

class JSONLabels:
    def __init__(self, config):
        self.location = config['DATA']['JSON']
    def load(self, idx):
        with open(os.path.join(self.location+str(idx)+'.json'), 'r') as f_:
            text = json.load(f_)
        text = text['responses'][0]['labelAnnotations']
        text = [(i['description'], i['score']) for i in text]

        return text

