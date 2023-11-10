import logging
from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from db import elastic
from settings import config
from settings.logger import LOGGING


@asynccontextmanager
async def lifespan(app: FastAPI):
    elstic_conf = config.ElasticsearchSettings()
    elastic.es = AsyncElasticsearch(
        hosts=[f'{elstic_conf.host}:{elstic_conf.port}']
    )
    yield
    await elastic.es.close()


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


if __name__ == '__main__':
    elstic_conf = config.ElasticsearchSettings()
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
