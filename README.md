# pubpulse

Someday, maybe an agent for finding good stuff in the firehose

## Quick start for local dev on MacOS

First, get Mastodon API credentials - e.g. at https://mastodon.social/settings/applications/new

Then, create env settings for your installation
  - copy `env-example` to `.env` and edit
  - adjust the API base URL to your instance's base URL
  - fill out the variables from the app - client key, client secret, access token

Finally, install dependencies and start up the mix of docker and host services:
```bash
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
./scripts/start-dev.sh
```

Somewhere in those startup messages, you should see a URL for a jupyter notebook. Open that in your browser and have fun!

## dev notes

- `docker compose exec -u root -ti db psql example postgres`
- [flask migrate docs](https://flask-migrate.readthedocs.io/en/latest/index.html)
  - `docker compose exec -ti bot flask db migrate -m'add ingested_at datestamp'`
  - `docker compose exec -ti bot flask db upgrade`

## TODO

- find a local embeddings model microservice that can use apple silicon GPU

- implement a command to auto-create a new app on a mastodon instance and initiate oauth dance?

- create directories on startup - db, notebook

- drop dependence on flask-migrate / alembic and switch to plain old SQL migrations?

- bot error - mastodon.errors.MastodonVersionError: Version check failed (Need version 1.1.0)
  - fixed by using correct API base URL
