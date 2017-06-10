# -*- coding: utf-8 -*-
import csv
import urllib.request
#from multiprocessing.dummy import Pool # use threads for I/O bound tasks
from multiprocessing import Pool
from urllib.request import urlretrieve

import os

import pandas as pd 

def convert_url_to_image(url):
    image_url = url.replace(".html", ".jpg")
    image_url = image_url.replace("html", "detail")
    return image_url

def convert_url_to_image_art(url):
    image_url = url.replace(".html", ".jpg")
    image_url = image_url.replace("html", "art")
    return image_url

def enrich_catalog(catalog_file):
    catalog = pd.read_csv(catalog_file, sep=";", encoding="cp1250")
    catalog["URL_image"] = catalog["URL"].apply(convert_url_to_image)
    catalog["URL_image_art"] = catalog["URL"].apply(convert_url_to_image_art)

    return catalog


###############################################################################
def gettingURLs():
    ressources=[]
    # Downloading images in images directory
    with open('catalog.csv', 'r',encoding='cp1250') as f:
        reader = csv.reader(f,delimiter=';')
        # Ignoring the first line (header)
        next(reader)
        index = 2
        for row in reader:
        
            # On modifie l'URL de la page afin de crée l'URL de l'image
            # Convertion du lien http://www.wga.hu/html/a/aagaard/rosegard.html
            # Vers la ressouce  http://www.wga.hu/detail/a/aagaard/rosegard.jpg            
            ressourceURL = row[6][:18]+'detail'+row[6][22:][:-5]+'.jpg'
            ressourceName = './images/' + str(index)+'.jpg'
            # Le nom de la ressource est n° de la ligne_auteur_titre
            # urllib.request.urlretrieve(ressourceURL,ressourceName)
            index +=1 
            ressources.append([ressourceURL,ressourceName])


    return (ressources)
###############################################################################
def downloadImages(ressources):
    try :
        #print("downloading :"+ressources[0]+" "+ressources[1])
        urllib.request.urlretrieve(ressources[0],ressources[1])
    except:
        print("ERROR :"+ressources[0]+" - " +ressources[1])

###############################################################################
# On split par paquet
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

###############################################################################
if __name__ == '__main__':
    if not os.path.exists("./images"):
        os.makedirs("./images")
    ressources = gettingURLs()
    # Téléchargement par paquet de ~10K
    ressourcesSplited = split_list(ressources,5)
    for i in range(len(ressourcesSplited)):
        print("#### Next split ####")
        with Pool(4) as p:
            p.map(downloadImages, ressourcesSplited[i])


"""
    for r in ressources :
        print("downloading :"+r[0]+" "+r[1])
        downloadImages(r)
"""
    
