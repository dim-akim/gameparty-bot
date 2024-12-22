import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import aliases, FROM, UNTIL, READY, UNREADY, CHECKED, PLUS, MINUS
from bot.utils.models import ReadyTime

logger = logging.getLogger(__name__)


def make_inline_keyboard(party: dict[str, ReadyTime],
                         callback_prefix: str = '') -> InlineKeyboardMarkup | None:
    keyboard = [[InlineKeyboardButton('ready', callback_data=f'{callback_prefix}&&{READY}'),
                InlineKeyboardButton(f'{MINUS}', callback_data=f'{callback_prefix}&&{MINUS}'),
                InlineKeyboardButton(f'{PLUS}', callback_data=f'{callback_prefix}&&{PLUS}')]]
    if len(party) > 0:
        for username, ready_time in party.items():
            keyboard.append(_make_user_row(username, ready_time, f'{callback_prefix}&{username}'))

    logger.debug(f'Constructed {keyboard} from {party}')
    return InlineKeyboardMarkup(keyboard)


def _make_user_row(username: str,
                   ready_time: ReadyTime,
                   callback_prefix: str = '') -> list[InlineKeyboardButton]:
    buttons = [InlineKeyboardButton(username, callback_data=f'{callback_prefix}&{UNREADY}'),
               InlineKeyboardButton(text=f'c {ready_time.since} {CHECKED * (ready_time.changing == FROM)}',
                                    callback_data=f'{callback_prefix}&{FROM}'),
               InlineKeyboardButton(f'по {ready_time.until} {CHECKED * (ready_time.changing == UNTIL)}',
                                    callback_data=f'{callback_prefix}&{UNTIL}')]

    return buttons
