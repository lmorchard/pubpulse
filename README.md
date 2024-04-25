# pubpulse

Someday, maybe an agent for finding good stuff in the firehose

## Quick start for local dev on MacOS with Apple Silicon

First, get Mastodon API credentials - e.g. at https://mastodon.social/settings/applications/new

Then, create env settings for your installation
  - copy `env-example` to `.env` and edit
  - adjust the API base URL to your instance's base URL
  - fill out the variables from the app - client key, client secret, access token

Next, make sure you have Docker Desktop installed.

Finally, install dependencies and start up the mix of docker and host services:
```bash
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
docker compose -f compose-dev.yaml build
./scripts/start-dev.sh
```

Somewhere in those startup messages, you should see a URL for a jupyter notebook. Open that in your browser and have fun!

## what comes in the box for local dev?

This project is a mix of services, mostly running in docker containers. A few things run on the host, mainly for access to the GPU in local development - particularly when using an Apple Silicon laptop.

Everything overall in local dev is started with `scripts/start-dev.sh`. This script uses Honcho with `Procfile-dev` to launch both a set of containers with Docker Compose (`compose-dev.yaml`) and a few host-side processes.

In docker, we have:

- db - a postgres database
- rabbitmq - a rabbitmq message broker for background tasks handled by Celery
- ingest-bot - a mastodon API client which subscribes to the public timeline and ingests messages into the database
- webapp - a flask app serving up a web-based user interface
- worker-general-cpu - a Celery worker for running general background tasks that only need CPU

On the host, we have:

- worker-ml-gpu - a Celery worker for running ML models on the host with GPU access
- local-ml-api - a Flask app serving up an API for running ML tasks on the host with GPU access
- host-notebook - a jupyter notebook server for tinkering with ML models with GPU access

Explore the `scripts` directory to see how all the above are started.

Someday, hopefully all the above can be deployed to cloud servers all in Docker containers.

## dev notes

- `docker compose exec -u root -ti db psql example postgres`
- [flask migrate docs](https://flask-migrate.readthedocs.io/en/latest/index.html)
  - `docker compose exec -ti bot flask db migrate -m'add ingested_at datestamp'`
  - `docker compose exec -ti bot flask db upgrade`

## TODO

- move notebook back into docker as a forcing-function to rely on local ML API for GPU-bound stuff?

- rabbitmq okay for production? move to redis or postgres for celery?

- implement a command to auto-create a new app on a mastodon instance and initiate oauth dance?

- create directories on startup - db, notebook

- drop dependence on flask-migrate / alembic and switch to plain old SQL migrations?

- bot error - mastodon.errors.MastodonVersionError: Version check failed (Need version 1.1.0)
  - fixed by using correct API base URL
