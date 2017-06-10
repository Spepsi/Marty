import wikipedia


def hello_world():
    res = wikipedia.page('hello')
    print(res.content)