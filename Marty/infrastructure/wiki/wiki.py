import wikipedia
"""
Moteur de recherche d'oeuvre
"""

def hello_world():
    res = wikipedia.page('la joconde')
    print(res.content)

def request_painting(author, title):
    try:
        wikipedia.set_lang('fr')
        request_ = title+" "+author
        res = wikipedia.page(request_)
    except:
        wikipedia.set_lang('en')
        request_ = title+" "+author
        res = wikipedia.page(request_)
    return res

def request_author(author):
    try:
        wikipedia.set_lang('fr')
        request_ = author
        res = wikipedia.page(request_)
    except:
        wikipedia.set_lang('en')
        request_ = author
        res = wikipedia.page(request_)
    return res