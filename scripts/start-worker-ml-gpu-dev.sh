#!/bin/bash
export MASTODON_AGENT_CELERY_BROKER_URL=amqp://localhost
export MASTODON_AGENT_CELERY_RESULTS_BACKEND=rpc://localhost

watchmedo auto-restart \
    --directory='.' \
    --recursive \
    --patterns='*.py' \
    --ignore-directories \
    --ignore-patterns='db/*;log/*' \
    ./scripts/start-worker-ml-gpu.sh
