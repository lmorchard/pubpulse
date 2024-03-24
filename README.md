# pubpulse

Someday, maybe an agent for finding good stuff in the firehose

## Usage

1. Get Mastodon API credentials:
1. Create a new application at your instance - e.g. https://mastodon.social/settings/applications/new
1. Create env settings for your installation
    - copy `env-example` to `.env` and edit 
    - adjust the API base URL to your instance's base URL
    - fill out the variables from the app - client key, client secret, access token
1. `docker compose up`
1. Visit the notebook at `http://127.0.0.1:8888/lab`

## dev notes

- [flask migrate docs](https://flask-migrate.readthedocs.io/en/latest/index.html)
  - `flask db migrate -m'add ingested_at datestamp'`
  - `flask db upgrade`

## TODO

- implement a command to auto-create a new app on a mastodon instance and initiate oauth dance?

- create directories on startup - db, notebook

- run migrations on DB creation
  - added migration run to bot startup

- permission error on `notebook/` directory when starting jupyterlab
  - chmod a+rw notebook

- bot error - mastodon.errors.MastodonVersionError: Version check failed (Need version 1.1.0)
  - fixed by using correct API base URL
