import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.ready import set_ready, set_unready
from bot.handlers.party import show_one_game
from bot.utils import ReadyMessage
from bot.config import READY, UNREADY

logger = logging.getLogger(__name__)


async def process_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    logger.debug(f'Button `{query.data}` pressed by user {update.effective_user.name}')
    current_user = update.effective_user.name
    day, game, user, command = query.data.split('&')
    if user and current_user != user:
        return await _wrong_user(update, context)

    await query.answer()
    if command == READY:
        if current_user in context.chat_data[day][game]:
            return
        await set_ready(current_user, ReadyMessage(game, day), context)
    elif command == UNREADY:
        await set_unready(user, ReadyMessage(game, day), context)
    elif context.chat_data[day][game].get(user):
        context.chat_data[day][game][user][command] = not context.chat_data[day][game][user][command]
    await show_one_game(game, day, update, context)


async def _wrong_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    logger.debug(f'Access to button `{query.data}` is restricted for user {update.effective_user.name}')
    await query.answer('Не твоя кнопка!')
