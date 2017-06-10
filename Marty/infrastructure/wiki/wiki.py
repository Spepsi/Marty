import wikipedia


def hello_world():
    res = wikipedia.page('la joconde')
    print(res.content)

def request_painting(author, title):
    request_ = title+" "+author
    res = wikipedia.page(request_)
    return res