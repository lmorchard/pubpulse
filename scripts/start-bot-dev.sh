#!/bin/sh
python3 -m flask --app mastodon_agent/webapp db upgrade
watchmedo auto-restart \
    --directory='.' \
    --recursive \
    --patterns='*.py' \
    --ignore-directories \
    --ignore-patterns='db/*;log/*' \
    ./scripts/start-bot.sh
