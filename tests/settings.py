from pydantic_settings import BaseSettings, SettingsConfigDict

ELASIC_INDEXES = ['movies', 'genres', 'persons']


class RedisSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 6379
    model_config = SettingsConfigDict(env_prefix='redis_')


class ElasticsearchSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 9200
    model_config = SettingsConfigDict(env_prefix='elastic_')


class CommonSettings(BaseSettings):
    api_url: str = 'http://api:8000'
