from celery import Celery

from ..config import config
from ..log import logger
from ..celery import app

@app.task(queue='ml_gpu')
def mult(x, y):
    return x * y
