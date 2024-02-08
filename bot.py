import logging
import mastodon.streaming

from agent_jumbo.mastodon_client import MastodonClient
from agent_jumbo.config import config
from agent_jumbo.logging import logger


def main():
    log = logging.getLogger("bot")

    print("Hello World!")
    print(f"{config.api_base_url}")

    client = MastodonClient(
        user_agent=config.user_agent,
        api_base_url=config.api_base_url,
        client_id=config.client_key,
        client_secret=config.client_secret,
        access_token=config.access_token,
        debug_requests=config.debug_requests,
    )

    client.stream_public(
        listener=BotStreamListener(client=client),
        reconnect_async=True
    )


class BotStreamListener(mastodon.streaming.StreamListener):
    def __init__(self, client):
        # self.bot = bot
        self.client = client
        self.logger = logging.getLogger("bot")

    def on_notification(self, notification):
        self.logger.debug(notification)

    def on_update(self, update):
        self.logger.debug(update)

    def on_status_update(self, update):
        self.logger.debug(update)


if __name__ == "__main__":
    main()
