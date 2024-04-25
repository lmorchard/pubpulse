import logging
import json
import time
import requests.exceptions
import mastodon.streaming
import mastodon.errors

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import psycopg2
from pgvector.psycopg2 import register_vector

from ..config import config
from ..log import logger
from ..models import db, Status
from ..tasks import ml_gpu

from .client import MastodonClient

from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def main():
    conn = psycopg2.connect(config.database_url)
    conn.autocommit = True
    register_vector(conn)

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
                listener=BotStreamListener(client=client, engine=engine, conn=conn),
                reconnect_async=True
            )
        except mastodon.errors.MastodonNetworkError as e:
            pass
        except requests.exceptions.SSLError as e:
            pass

        time.sleep(10)


class BotStreamListener(mastodon.streaming.StreamListener):
    def __init__(self, client, engine, conn):
        # self.bot = bot
        self.client = client
        self.logger = logging.getLogger("bot")
        self.engine = engine
        self.conn = conn

    def on_update(self, status):
        self.upsert_status(status)

    def on_status_update(self, status):
        self.upsert_status(status)

    def on_delete(self, status_id):
        # todo: handle status deletion - delete from DB and embedding and anywhere else the status ended up processed
        self.logger.debug(f"Delete {status_id}")
        """
        with Session(self.engine) as session:
            session.query(Status).filter(Status.url == status_id).delete()
            session.commit()
        """

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

        # todo: defer this into a CPU worker background task
        # todo: also, figure out how to do this with SQLAlchemy ORM? or use raw SQL above
        # todo: batch these up into larger jobs?
        embeddings = ml_gpu.embed.delay([status.content]).get(timeout=10)
        cur = self.conn.cursor()
        cur.execute(
            """
                INSERT INTO status_embeddings (url, embedding) VALUES (%s, %s)
                    ON CONFLICT (url) DO UPDATE SET embedding = EXCLUDED.embedding;
            """,
            (status.url, embeddings[0])
        )
        cur.close()


if __name__ == "__main__":
    main()
