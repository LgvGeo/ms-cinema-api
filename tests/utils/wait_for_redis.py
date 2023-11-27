import time

from redis import Redis

from tests.settings import RedisSettings

if __name__ == '__main__':
    redis_conf = RedisSettings()
    redis_client = Redis(host=redis_conf.host, port=redis_conf.port)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
