import logging.config
import os

CURRENT_DIR = os.getcwd()
print(CURRENT_DIR)
os.makedirs(CURRENT_DIR + r'\logs', exist_ok=True)

LOG_CONF = {
    'version'   : 1,
    'formatters': {
        'file_form'   : {
            'format': '%(asctime)s - %(levelname)-8s - %(funcName)-22s - %(message)s'
            },
        'console_form': {
            'format': '%(levelname)-8s - %(message)s'
            },
        },
    'handlers'  : {
        'console_hand' : {
            'class'    : 'logging.StreamHandler',
            'stream'   : 'ext://sys.stdout',
            'level'    : 'INFO',
            'formatter': 'console_form',
            },
        'file_hand_rot': {
            'class'      : 'logging.handlers.RotatingFileHandler',
            'filename'   : os.path.join(CURRENT_DIR, 'logs', 'label_maker.log'),
            'maxBytes'   : 3_145_728,  # 3MB
            'backupCount': 5,  # five files with log backup
            'level'      : 'DEBUG',
            'encoding'   : 'utf-8',
            'formatter'  : 'file_form',
            },
        },
    'loggers'   : {
        'root': {
            'handlers': ['console_hand', 'file_hand_rot'],
            'level'   : 'DEBUG',
            }
        }
    }


def setup_logging():
    logging.config.dictConfig(LOG_CONF)
    log = logging.getLogger(__name__)
    log.debug('Logging was set up.')
