import dill

from naggy import redis


def publish(channel, data):
    redis.publish(channel, dill.dumps(data))
