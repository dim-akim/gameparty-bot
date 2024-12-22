"""
Здесь собираются
    Общие настройки бота
    Алиасы для разных игр, времени, дней недели и продолжительности игры
"""
import os
import json
import logging
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s | %(levelname)-7s | %(name)-30s [%(lineno)4d] - %(message)s",
        level=level
    )
    logging.getLogger('httpx').setLevel(level + 10)
    logging.getLogger('httpcore').setLevel(level + 10)


APP_ENV = os.getenv('APP_ENV')
BASE_DIR = Path.cwd()
WORKDIR = BASE_DIR / 'bot'
PERSISTENCE_FILE = 'persistence.pickle'

# Telegram-бот
BOT_TOKEN = os.getenv('BOT_TOKEN')
ECHO_TOKEN = os.getenv('ECHO_TOKEN')

SUPERUSER_ID = int(os.getenv('SUPERUSER_ID'))
SUPERUSER_USERNAME = os.getenv('SUPERUSER_USERNAME')

CALLBACK_PREFIX = ''

# Слова-псевдонимы
ALIASES_FILE = 'aliases.json'
with open(WORKDIR / ALIASES_FILE, encoding='utf-8') as file:
    aliases = json.load(file)

DEFAULT = aliases.pop('default')
NUMERALS = aliases.pop('numerals')
GAME, DAY, WEEKDAY, TIME, OTHER = aliases.keys()
FROM, UNTIL, AT, FOR, HOUR, HOURS = aliases[OTHER].keys()

READY = 'ready'
UNREADY = 'unready'
NOT_RESOLVED = 'not_resolved'
AMOUNTS = [
    '1',
    '2',
    'два',
    'пару',
    '3',
    'три'
]

CHECKED = '✅'
PLUS = '➕'
MINUS = '➖'

TIMESTAMP = '%d.%m.%Y'
