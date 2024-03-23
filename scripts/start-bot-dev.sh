#!/bin/sh
flask db upgrade
watchmedo auto-restart \
    --directory='.' \
    --recursive \
    --patterns='*.py' \
    --ignore-directories \
    --ignore-patterns='db/*;log/*' \
    python3 bot.py
