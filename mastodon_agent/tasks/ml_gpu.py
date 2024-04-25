from celery import Celery

from ..config import config
from ..log import logger
from ..celery import app


@app.task()
def embed(texts):
    embedding_model = get_embedding_model()
    embeddings = embedding_model.encode(texts)
    return embeddings.tolist()


embedding_model = None
def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    return embedding_model
