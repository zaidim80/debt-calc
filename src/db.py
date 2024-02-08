from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from config import cfg


dbe = create_async_engine(cfg.dsn)


async def get_connection() -> AsyncConnection:
    async with dbe.begin() as dbc:
        yield dbc
