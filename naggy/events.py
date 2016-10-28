import logging
import time

from naggy import redis_pubsub


def process_events():
    logging.info("processing events")
    while True:
        redis_pubsub.get_message()
        # it seems like events with callbacks doesn't return anything?
        time.sleep(1)
