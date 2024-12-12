import logging
from datetime import date

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.utils import (ReadyMessage, ResolvedMessage,
                       make_inline_keyboard, log_entry_with_several_lines)
from bot.config import TIMESTAMP, CALLBACK_PREFIX, default_ready, GAME

logger = logging.getLogger(__name__)


async def party_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f'Command /party is triggered by {update.effective_user}')
    args = context.args
    if args:
        resolved = ResolvedMessage.from_list(context.args)
        if not resolved.day and not resolved.weekday:
            return await say_incorrect_day(update, context)
        else:
            day = ReadyMessage.from_resolved(resolved).day
    else:
        day = date.today().strftime(TIMESTAMP)
    return await show_party(day, update, context)


async def show_party(day: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    games = context.chat_data.get(day, {})
    if not games:
        context.chat_data[day] = games
        context.chat_data[day][default_ready[GAME]] = {}
        return await show_one_game(default_ready[GAME], day, update, context)
    for game in games:
        await show_one_game(game, day, update, context)


async def say_incorrect_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f'{context.args} has not a valid day or weekday')
    text = ('Не могу разобрать, что за день такой:\n'
            f'{" ".join(context.args)}\n'
            '\n'
            'Я могу понять <i>дни недели</i> или слова: <i>сегодня</i>, <i>завтра</i>, <i>послезавтра</i>:\n'
            '\n'
            '/party\n'
            '<code>/party завтра</code>\n'
            '<code>/party в четверг</code>\n')
    await context.bot.send_message(
        update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML
    )


async def show_one_game(game: str, day: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(log_entry_with_several_lines(game, day, context))
    players_amount = len(context.chat_data[day][game])
    text = (f'<code>Дата:    </code>{day}\n'
            f'<code>Игра:    </code>{game}\n'
            f'\n'
            f'<code>Игроков: </code>{players_amount} из 5\n')
    if players_amount > 0:
        text += (
            f'\n'
            f'Нажми на кнопки с тем временем, в которое ты готов играть.\n'
            f'Нажми еще раз, чтобы снять отметку.\n'
            f'Нажми на свой ник, чтобы выйти из пати.\n')
    keyboard = make_inline_keyboard(context.chat_data[day][game], f'{CALLBACK_PREFIX}{day}&{game}')
    query = update.callback_query
    if query:
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
    else:
        await context.bot.send_message(
            update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
