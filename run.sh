#!/bin/bash

source venv/bin/activate
export DISCORD_TOKEN="$(cat discord_token.txt)"
python3 bot.py
