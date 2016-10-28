import logging
import logging.config
import os

from redis import StrictRedis
from slackbot import settings
from slackbot.slackclient import SlackClient

from config import Config, configs

config = Config()
conf = os.getenv('APP_CONFIG', 'default')
config.from_object(configs[conf])

# must be loaded after `config`
from naggy.providers import GitHubProvider

provider = GitHubProvider()
redis = StrictRedis()
redis_pubsub = redis.pubsub(ignore_subscribe_messages=True)

slack_client = SlackClient(settings.API_TOKEN, connect=False)
slack_client.login_data = {
    'self': {'name': config['SLACK_BOT_NAME']}
}

from naggy import callbacks


def setup():
    logging.config.dictConfig(config['LOGGING_CONFIG'])
    logging.info("using config: %s" % conf)

    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('slackbot').setLevel(logging.ERROR)

    for channel, callback in config['PUBSUB_CHANNELS']:
        redis_pubsub.subscribe(**{channel: eval(callback)})
