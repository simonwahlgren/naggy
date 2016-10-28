import logging
import re

from slackbot.bot import respond_to, listen_to


@respond_to('^naggy', re.IGNORECASE)
def naggy(message):
    logging.info('respond_to: naggy')
    message.reply("Hurray!")
