import os
import configparser

class Config:
    def __new__(self, file=None):
        config = configparser.ConfigParser()

        # we use the config.ini file in the same repository as default
        if file is None:
            file = "config.ini"
        else:
            if not os.path.exists(file):
                raise IOError("File {} does not exist".format(file))
        config.read(file)
        return config
