#!/bin/bash
watchmedo auto-restart \
    --directory='.' \
    --recursive \
    --patterns='*.py' \
    --ignore-directories \
    --ignore-patterns='db/*;log/*' \
    ./scripts/start-worker-general-cpu.sh
