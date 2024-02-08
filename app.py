from flask import Flask
from agent_jumbo.config import config
from agent_jumbo.logging import logger

app = Flask(__name__)

@app.route('/')
def hello_world():
    logger.debug("HI THERE")
    return 'Hello, World!'