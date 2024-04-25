#!/bin/bash
export FLASK_APP=mastodon_agent.webapp

python3 -m flask run --debug --host=0.0.0.0 --port=${PORT}
