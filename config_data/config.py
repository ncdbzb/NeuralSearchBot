from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Database:
    db_name: str


@dataclass
class Channel:
    channel_id: str


@dataclass
class Config:
    tg_bot: TgBot
    db: Database
    channel: Channel


def load_config(path: str | None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN'),
                     admin_ids=list(map(int, env.list('ADMIN_IDS')))),
        db=Database(db_name=env('DB_NAME')),
        channel=Channel(channel_id=env('CHANNEL_ID')))
