#!/bin/bash
mkdir -p notebook/{config,data,runtime}

export JUPYTER_CONFIG_DIR=notebook/config
export JUPYTER_DATA_DIR=notebook/data
export JUPYTER_RUNTIME_DIR=notebook/runtime

export MASTODON_AGENT_DATABASE_URL=postgresql://postgres:8675309jenny@localhost:55432/example
export MASTODON_AGENT_DEBUG=True
export MASTODON_AGENT_EMBEDDINGS_API_URL=http://127.0.0.1:8674/predictions/my_model
export MASTODON_AGENT_CELERY_BROKER_URL=amqp://localhost
export MASTODON_AGENT_CELERY_RESULTS_BACKEND=rpc://localhost
export MASTODON_AGENT_ML_API_URL=http://127.0.0.1:8673

./venv/bin/jupyter lab
