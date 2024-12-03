import logging

from redis import Redis
from django.conf import settings


class redis_service:
    def __init__(self):
        try:
            self.redis = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
            )
        except Exception as e:
            logging.error(f"Error connecting to Redis: {e}")
            raise

    def set(self, key, value):
        try:
            self.redis.set(key, value)
        except Exception as e:
            logging.error(f"Error setting key {key}: {e}")

    def get(self, key):
        try:
            return self.redis.get(key)
        except Exception as e:
            logging.error(f"Error getting key {key}: {e}")
            return None

    def delete(self, key):
        try:
            self.redis.delete(key)
        except Exception as e:
            logging.error(f"Error deleting key {key}: {e}")

    def keys(self):
        try:
            return self.redis.keys()
        except Exception as e:
            logging.error(f"Error fetching keys: {e}")
            return []

    def flush(self):
        try:
            self.redis.flushdb()
        except Exception as e:
            logging.error(f"Error flushing database: {e}")
