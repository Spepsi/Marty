from Marty.utils.config.config import  Config
from Marty.infrastructure.loader.loader import JSONLabels
config = Config(file='../../config.ini')
json_ = JSONLabels(config)

from pdb import set_trace; set_trace()