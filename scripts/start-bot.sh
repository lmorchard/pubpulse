#!/bin/sh
python3 -m flask --app mastodon_agent/webapp db upgrade
python3 -m mastodon_agent.bot
