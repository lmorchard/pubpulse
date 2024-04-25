#!/bin/bash
celery \
  --app mastodon_agent.tasks.general_cpu \
  worker \
  --queues general_cpu \
  --loglevel=INFO
