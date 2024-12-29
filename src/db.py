from sqlalchemy.ext.asyncio import create_async_engine
# import redis.asyncio as redis

from config import cfg


dbe = create_async_engine(cfg.dsn)
# rds = redis.Redis(host=cfg.redis, encoding="utf-8", decode_responses=True)


async def get_connection():
    async with dbe.begin() as dbc:
        yield dbc
