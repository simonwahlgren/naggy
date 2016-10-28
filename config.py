import os

from pathlib import Path
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config(dict):

    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


class BaseConfig:
    DEBUG = False

    LOG_ROOT = str(Path(os.path.dirname(__file__)).parent)
    LOG_ROOT = os.path.join(LOG_ROOT, 'logs')

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        }
    }

    GITHUB_ORG = 'fyndiq'
    GITHUB_REPO = 'fyndiq'
    GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
    GITHUB_PASSWORD = os.environ.get('GITHUB_PASSWORD')

    PUBSUB_CHANNELS = [
        ('get_rfr_issues', 'callbacks.process_get_rfr_issues'),
    ]

    SLACK_DEFAULT_CHANNEL = 'testroom'
    SLACK_BOT_NAME = 'boom'


class DevConfig(BaseConfig):
    DEBUG = True

configs = {
    'default': BaseConfig,
    'dev': DevConfig,
}
