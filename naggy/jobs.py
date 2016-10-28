import logging
import schedule
import time

from naggy import provider
from naggy.pubsub import publish


def get_rfr_issues():
    data = provider.get_issues()
    publish('get_rfr_issues', data)


schedule.every(10).seconds.do(get_rfr_issues)


def schedule_jobs():
    logging.info("starting job scheduler")
    while True:
        schedule.run_pending()
        time.sleep(1)
