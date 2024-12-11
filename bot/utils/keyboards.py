import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import aliases, READY_FROM, READY, UNREADY

logger = logging.getLogger(__name__)


def make_inline_keyboard(game_dict: dict[str, dict],
                         callback_prefix: str = '') -> InlineKeyboardMarkup | None:
    keyboard = [[InlineKeyboardButton('Присоединиться', callback_data=f'{callback_prefix}&&{READY}')]]
    if len(game_dict) > 0:
        for username, time_dict in game_dict.items():
            keyboard.extend(_make_user_rows(username, time_dict, f'{callback_prefix}&{username}'))

    logger.debug(f'Constructed {keyboard} from {game_dict}')
    return InlineKeyboardMarkup(keyboard)


def _make_user_rows(username: str,
                    time_dict: dict[str, bool],
                    callback_prefix: str = '') -> tuple[list[InlineKeyboardButton], list[InlineKeyboardButton]]:
    hours = list(aliases[READY_FROM].keys())
    buttons_1st_row = [InlineKeyboardButton(username, callback_data=f'{callback_prefix}&{UNREADY}')]
    buttons_1st_row += [
        InlineKeyboardButton(hour + '✔' * time_dict[hour], callback_data=f'{callback_prefix}&{hour}')
        for hour in hours[:2]
    ]
    buttons_2nd_row = [
        InlineKeyboardButton(hour + '✔' * time_dict[hour], callback_data=f'{callback_prefix}&{hour}')
        for hour in hours[2:]
    ]

    return buttons_1st_row, buttons_2nd_row
