import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def read_int(name: str, default: int = 0) -> int:
    try:
        return int(os.getenv(name, "").strip())
    except (TypeError, ValueError):
        return default

@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: tuple[int, ...]
    group_id: int
    bot_name: str
    prefix: str
    timezone: str
    database_path: str

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "PUT_YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("Заполните BOT_TOKEN в .env")

    admins = tuple(
        x for x in (
            read_int("ADMIN_ID_1"),
            read_int("ADMIN_ID_2"),
            read_int("ADMIN_ID_3"),
            read_int("ADMIN_ID_4"),
            read_int("ADMIN_ID_5"),
        ) if x
    )
    if not admins:
        raise RuntimeError("Нужно указать хотя бы один ADMIN_ID_*")

    return Config(
        bot_token=token,
        admin_ids=admins,
        group_id=read_int("GROUP_ID"),
        bot_name=os.getenv("BOT_NAME", "The Endy • Genshin"),
        prefix=os.getenv("COMMAND_PREFIX", ".те"),
        timezone=os.getenv("TIMEZONE", "Europe/Stockholm"),
        database_path=os.getenv("DATABASE_PATH", "data/endy.db"),
    )

config = load_config()
