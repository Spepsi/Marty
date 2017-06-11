import json
import os



class UrlComparator:
    def __init__(self, labels_to_compare):
        self.labels_to_compare = labels_to_compare
    def __call__(self, labels):
        labs = set([description for description, score in labels])
        labs2 = set([description for description, score in self.labels_to_compare])
        return labs==labs2

class LabelsComparator:
    def __init__(self, labels_to_compare):
        self.labels_to_compare = labels_to_compare
    def __call__(self, labels):
        labs = set([description for description, score in labels])
        labs2 = set([description for description, score in self.labels_to_compare])
        print(labs, labs2)
        return labs==labs2

class JSONLabels:
    def __init__(self, config):
        self.location = config['DATA']['JSON']
    def load(self, idx):
        with open(os.path.join(self.location, str(idx)+'.json'), 'r') as f_:
            text = json.load(f_)
        text = text['responses'][0]['labelAnnotations']
        text = [(i['description'], i['score']) for i in text]
        return text

class JSONColors:
    def __init__(self, config):
        self.location = config['DATA']['JSON']
    def load(self, idx):
        with open(os.path.join(self.location, str(idx)+'.json'), 'r') as f_:
            text = json.load(f_)
        colors = text['responses'][0]['imagePropertiesAnnotation']["dominantColors"]["colors"]
        colors = [tuple(color["color"].values()) for color in colors][:3]
        colors = tuple(colors)
        return colors

class JSONWebEntities:
    def __init__(self, config):
        self.location = config['DATA']['JSON']
    def load(self, idx):
        with open(os.path.join(self.location, str(idx)+'.json'), 'r') as f_:
            text = json.load(f_)
        web_entities = text['responses'][0]['webDetection']["webEntities"]
        web_entities = [web_entity["description"] for web_entity in web_entities]
        web_entities = web_entities[:5]
        web_entities = web_entities + [np.nan for _ in range(5 - len(web_entities))]
        web_entities = tuple(web_entities)
        return web_entities


class JSONUrls:
    def __init__(self, config):
        self.location = config['DATA']['JSON']
    def load(self, idx):
        with open(os.path.join(self.location+str(idx)+'.json'), 'r') as f_:
            text = json.load(f_)
        text = text['responses'][0]['webDetection']['partialMatchingImages']
        text = [i['url'] for i in text]
        return text

class JSONSafeSearch:
    def __init__(self, config):
        self.location = config['DATA']['JSON']
    def load(self, idx):
        with open(os.path.join(self.location+str(idx)+'.json'), 'r') as f_:
            text = json.load(f_)
        text = text['responses'][0]['safeSearchAnnotation']
        return text
