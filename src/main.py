import logging
import logging.config
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import cfg
from logger import LOGGING


logging.config.dictConfig(LOGGING)
log = logging.getLogger()


app = FastAPI(
    title='Калькулятор долгов',
    version='0.1',
    default_response_class=ORJSONResponse,
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=cfg.host,
        port=cfg.port,
    )
