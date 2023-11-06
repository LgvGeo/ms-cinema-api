import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from settings.logger import LOGGING

logging_config.dictConfig(LOGGING)


class RedisSettings(BaseSettings):
    host: str = Field(default='127.0.0.1', validation_alias='REDIS_HOST')
    port: str = Field(default='6379', validation_alias='REDIS_PORT')


class ElasticsearchSettings(BaseSettings):
    host: str = Field(
        default='127.0.0.1',
        validation_alias='ELASTIC_HOST')
    port: str = Field(
        default='9200',
        validation_alias='ELASTIC_PORT')


class CommonSettings(BaseSettings):
    project_name: str = Field(
        default='movies',
        validation_alias='PROJECT_NAME')
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
