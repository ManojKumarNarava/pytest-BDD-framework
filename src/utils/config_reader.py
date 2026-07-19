import configparser
from pathlib import Path


CONFIG_PATH = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "config.ini"
)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


def get_browser() -> str:
    return config.get("browser", "browser", fallback="chromium")


def is_headless() -> bool:
    return config.getboolean("browser", "headless", fallback=False)


def get_timeout() -> int:
    return config.getint("browser", "timeout", fallback=30000)


def get_base_url(environment: str = "qa") -> str:
    if not config.has_section(environment):
        raise ValueError(f"Environment '{environment}' is not configured.")

    return config.get(environment, "base_url")