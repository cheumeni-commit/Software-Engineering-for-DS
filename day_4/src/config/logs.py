# src/config/logs.py

# NOTE:
# We are using the context object here... As such, the logging
# can't be configured in src/__init__.py anymore

import logging.config

from src.context import context

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': (
                '[%(asctime)s] %(levelname)s - %(message)s'
            ),
            'datefmt': LOG_DATE_FORMAT
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': 'INFO',
            'filename': f'{context.dirs.logs}/acme.log',  # TODO: add this directory to the _Directories class
        },
    },
    'loggers': {
        'src': {
            'handlers': ['stdout', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        '': {  # default logger, used for, eg, 3rd-party lib
            'handlers': ['stdout'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)