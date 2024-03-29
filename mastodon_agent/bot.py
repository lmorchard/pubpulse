import logging
import json
import time
import requests.exceptions
import mastodon.streaming
import mastodon.errors

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .client import MastodonClient
from .config import config
from .log import logger
from .models import db, Status


from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def main():
    log = logging.getLogger("bot")

    engine = create_engine(
        config.database_url,
        json_serializer=lambda obj: json.dumps(obj, default=json_serial, ensure_ascii=False),
        json_deserializer=lambda obj: json.loads(obj, ensure_ascii=False)
    )

    client = MastodonClient(
        user_agent=config.user_agent,
        api_base_url=config.api_base_url,
        client_id=config.client_key,
        client_secret=config.client_secret,
        access_token=config.access_token,
        debug_requests=config.debug_requests,
    )

    while True:
        try:
            client.stream_public(
                listener=BotStreamListener(client=client, engine=engine),
                reconnect_async=True
            )
        except mastodon.errors.MastodonNetworkError as e:
            pass
        except requests.exceptions.SSLError as e:
            pass

        time.sleep(10)


class BotStreamListener(mastodon.streaming.StreamListener):
    def __init__(self, client, engine):
        # self.bot = bot
        self.client = client
        self.logger = logging.getLogger("bot")
        self.engine = engine

    def on_update(self, status):
        self.upsert_status(status)

    def on_status_update(self, status):
        self.upsert_status(status)

    def upsert_status(self, status):
        self.logger.debug(status.url)
        with Session(self.engine) as session:
          insert_stmt = insert(Status).values(url = status.url, status = status)
          upsert_stmt = insert_stmt.on_conflict_do_update(
              index_elements=['url'],
              set_={'status': insert_stmt.excluded.status}
          )
          session.execute(upsert_stmt)
          session.commit()


if __name__ == "__main__":
    main()
