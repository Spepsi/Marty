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
