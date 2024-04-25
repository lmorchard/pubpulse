#!/bin/bash
# solo worker pool is used to ensure single-threaded use of GPU
celery \
  --app mastodon_agent.tasks.ml_gpu \
  worker \
  --pool solo \
  --concurrency 1 \
  --queues ml_gpu \
  --loglevel=INFO
