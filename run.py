#!/usr/bin/env python3.5

import logging
import logging.config

from threading import Thread

from slackbot.bot import Bot

from naggy import setup
from naggy.jobs import schedule_jobs
from naggy.events import process_events


def run_bot():
    bot = Bot()
    bot.run()


callbacks = (
    # run_bot,
    # foobar,
    schedule_jobs,
    process_events,
)


def start_threads():
    for callback in callbacks:
        logging.info("running thread with callback: %s", callback.__name__)
        t = Thread(target=callback)
        t.daemon = True
        t.start()

    while True:
        pass


if __name__ == '__main__':
    setup()
    start_threads()
