#!/bin/bash
mkdir -p notebook/{config,data,runtime}

export JUPYTER_CONFIG_DIR=notebook/config
export JUPYTER_DATA_DIR=notebook/data
export JUPYTER_RUNTIME_DIR=notebook/runtime

export DATABASE_URL=postgresql://postgres:8675309jenny@localhost:55432/example

./venv/bin/jupyter lab
