import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.logger import LOGGING

logging_config.dictConfig(LOGGING)


class RedisSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 6379
    model_config = SettingsConfigDict(env_prefix='redis_')


class ElasticsearchSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 9200
    model_config = SettingsConfigDict(env_prefix='elastic_')


class CommonSettings(BaseSettings):
    project_name: str = 'movies'
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
