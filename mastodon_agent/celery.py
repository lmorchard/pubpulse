from celery import Celery
from .config import config

app = Celery(
    'mastodon_agent',
    broker=config.celery_broker_url,
    backend=config.celery_results_backend,
    broker_connection_retry_on_startup=True
)

app.conf.task_routes = {
  'mastodon_agent.tasks.ml_gpu.*': {'queue': 'ml_gpu'},
  'mastodon_agent.tasks.general_cpu.*': {'queue': 'general_cpu'},
}
