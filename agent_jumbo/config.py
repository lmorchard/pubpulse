import os
from dataclasses import dataclass, fields
from dotenv import dotenv_values

ENV_PREFIX = "AGENT_JUMBO"

@dataclass
class Config:
    log_level: str = "INFO"
    log_filename: str = ""
    log_maxbytes: int = 100000
    log_backup_count: int = 10

    debug: bool = False

    database_url: str = ""

    api_base_url: str = ""
    client_key: str = ""
    client_secret: str = ""
    access_token: str = ""

    hf_token: str = ""

    user_agent: str = "Agent Jumbo 0.1"
    debug_requests: bool = False

    def __init__(self, raw_config={}):
        for field in fields(Config):
            env_name = f"{ENV_PREFIX}_{field.name.upper()}"
            if env_name in raw_config:
                setattr(self, field.name, raw_config[env_name])


config = Config({
    **dotenv_values(".env"),
    **os.environ
})
