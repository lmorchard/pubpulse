from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from agent_jumbo.config import config
from agent_jumbo.logging import logger
from agent_jumbo.models import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    logger.debug("HI THERE")
    return 'Hello, World!'