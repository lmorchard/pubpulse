import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sentence_transformers import SentenceTransformer

from .config import config
from .log import logger
from .models import db


app = Flask(__name__)
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


@app.route('/')
def root():
    return 'Hello'


@app.route('/embeddings', methods=['POST'])
def embedding():
    data = request.get_json()
    chunks = data['inputs']
    logger.info("Received embeddings request with %d chunks", len(chunks))
    embeddings = embedding_model.encode(chunks)
    return jsonify(embeddings.tolist())

