from celery import Celery

from ..config import config
from ..log import logger
from ..celery import app

@app.task(queue='general_cpu')
def add(x, y):
    return x + y
