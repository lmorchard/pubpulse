#!/bin/sh
flask db upgrade
python3 bot.py