import logging
from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from uvicorn.workers import UvicornWorker

from api.v1 import films, genres, persons
from db import elastic, redis
from settings import config
from settings.logger import LOGGING


@asynccontextmanager
async def lifespan(app: FastAPI):
    elstic_conf = config.ElasticsearchSettings()
    redis_conf = config.RedisSettings()
    elastic.es = AsyncElasticsearch(
        hosts=[f'{elstic_conf.host}:{elstic_conf.port}']
    )
    redis.redis = Redis(host=redis_conf.host, port=redis_conf.port)
    yield
    await elastic.es.close()
    await redis.redis.close()


app = FastAPI(
    title=config.CommonSettings().project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])


class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": LOGGING,
        "log_level": logging.DEBUG
    }
