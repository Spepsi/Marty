import sys

sys.path.append('../') # Pour avoir accès à l'API


import wikipedia

res = wikipedia.page('hello')
print(res.content)
from pdb import set_trace; set_trace()

