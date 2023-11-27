import asyncio
import json
from typing import NamedTuple

import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from redis.asyncio import Redis

from tests.settings import (ELASIC_INDEXES, CommonSettings,
                            ElasticsearchSettings, RedisSettings)
from tests.testdata.genres_data import GENRES_DATA
from tests.testdata.movies_data import MOVIES_DATA
from tests.testdata.persons_data import PERSONS_DATA


class Response(NamedTuple):
    body: dict
    headers: dict
    status: int


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', name='elastic')
async def get_elastic_connection():
    elstic_conf = ElasticsearchSettings()
    elastic_conn = AsyncElasticsearch(
        hosts=[f'{elstic_conf.host}:{elstic_conf.port}']
    )
    yield elastic_conn
    await elastic_conn.close()


@pytest_asyncio.fixture(scope='session', name='redis')
async def get_redis_connection():
    redis_conf = RedisSettings()
    redis_conn = Redis(host=redis_conf.host, port=redis_conf.port)
    yield redis_conn
    await redis_conn.close()


@pytest_asyncio.fixture(scope='session', name='client')
async def get_client():
    common_settings = CommonSettings()
    session = ClientSession(common_settings.api_url)
    yield session
    await session.close()


async def create_elastic_index(name, connection: AsyncElasticsearch):
    with open(f'./testdata/{name}_index.json') as f:
        data = json.load(f)
    await connection.indices.create(name, data)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_indexes(elastic: AsyncElasticsearch):
    for index in ELASIC_INDEXES:
        await create_elastic_index(index, elastic)
    yield
    for index in ELASIC_INDEXES:
        await elastic.indices.delete(index)


@pytest_asyncio.fixture(scope='session')
async def insert_data_in_elastic(elastic):
    async def inner(index, data: list[dict]):
        actions = []
        for document in data:
            obj = {
                "_index": index,
                "_id": document['id'],
                "_source": document
            }
            actions.append(obj)
        await async_bulk(client=elastic, actions=actions, refresh='wait_for')
    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
async def generate_movies_data(insert_data_in_elastic):
    await insert_data_in_elastic('movies', MOVIES_DATA)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def generate_genres_data(insert_data_in_elastic):
    await insert_data_in_elastic('genres', GENRES_DATA)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def generate_persons_data(insert_data_in_elastic):
    await insert_data_in_elastic('persons', PERSONS_DATA)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def get_data(client: ClientSession):
    async def inner(url, params=None):
        params = params or {}
        async with client.get(url, params=params) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return Response(body, headers, status)
    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
async def get_data_from_cache(redis: Redis):
    async def inner(key):
        data = json.loads(await redis.get(key))
        return data
    return inner
