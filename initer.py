import json
import os
import sys

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))


log_conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s'
            }
        },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
            }
        },
    'loggers': {
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler'],
            'propagate': False
            },
        'same_hierarchy': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler'],
            'propagate': False
            },
        'lower.sub': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler'],
            'propagate': False
            }
        },
    'root': {'level': 'DEBUG'}
}


lan_conf = {
    "name": "default language pack",
    "language": "ja"
}


def check():
    DATAPATH = os.path.join(PATH, "data")
    if not os.path.isdir(DATAPATH):
        os.mkdir(os.path.join(DATAPATH, "config"))
        os.mkdir(os.path.join(DATAPATH, "setting"))
        with open(os.path.join(DATAPATH, "config", "logger.json"),
                  "w",
                  encoding="utf-8") as f:
            json.dump(f, log_conf)

        with open(os.path.join(DATAPATH, "setting", "acc.json"),
                  "w",
                  encoding="utf-8") as f:
            f.write("dwl")

        with open(os.path.join(DATAPATH, "setting", "api.json"),
                  "w",
                  encoding="utf-8") as f:
            f.write("dwl")

        with open(os.path.join(DATAPATH, "setting", "api.json"),
                  "w",
                  encoding="utf-8") as f:
            json.dump(f, lan_conf)
