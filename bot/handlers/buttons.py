import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.ready import set_ready, set_unready
from bot.handlers.party import show_one_game
from bot.utils import ReadyMessage, ReadyTime
from bot.config import READY, UNREADY, FROM, UNTIL, PLUS, MINUS

logger = logging.getLogger(__name__)


async def process_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    logger.debug(f'Button `{query.data}` pressed by user {update.effective_user.name}')
    current_user = update.effective_user.name
    day, game, user, command = query.data.split('&')
    if user and current_user != user:
        return await _wrong_user(update, context)
    await query.answer()

    party = context.chat_data[day][game]
    if current_user not in party and command in (READY, PLUS, MINUS):
        await set_ready(current_user, ReadyMessage(game, day), context)
    elif command == UNREADY:
        await set_unready(user, ReadyMessage(game, day), context)
    elif current_user in party:
        ready_time: ReadyTime = context.chat_data[day][game].get(current_user)
        if command == READY or command == ready_time.changing:
            logger.info(f'Ignored: pressed `{command}` on {ready_time} by {current_user}')
            return
        if command in (FROM, UNTIL):
            ready_time.changing = command
        elif command in (PLUS, MINUS):
            ready_time.update(command)

    await show_one_game(game, day, update, context)


async def _wrong_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    logger.debug(f'Access to button `{query.data}` is restricted for user {update.effective_user.name}')
    await query.answer('Не твоя кнопка!')
