#!/bin/bash
export FLASK_APP=mastodon_agent.ml.local_api_app
python3 -m flask run --debug --host=0.0.0.0 --port=${MLAPI_PORT:-8763}
