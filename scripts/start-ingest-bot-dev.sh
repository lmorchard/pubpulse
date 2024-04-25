#!/bin/sh
watchmedo auto-restart \
    --directory='.' \
    --recursive \
    --patterns='*.py' \
    --ignore-directories \
    --ignore-patterns='db/*;log/*' \
    ./scripts/start-ingest-bot.sh
