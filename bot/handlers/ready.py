import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import UNTIL
from bot.utils.models import ReadyMessage, ResolvedMessage, ReadyTime
from bot.handlers.party import show_party

logger = logging.getLogger(__name__)


async def ready(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug(f'Command /ready is triggered by {update.effective_user}')
    ready_message: ReadyMessage = ReadyMessage.from_resolved(
        ResolvedMessage.from_list(context.args)
    )
    data = context.chat_data
    day = ready_message.day
    game = ready_message.game

    if day not in data:
        data[day] = {}
    if game not in data[day]:
        data[day][game] = {}

    await set_ready(update.effective_user.name, ready_message, context)
    return await show_party(day, update, context)


async def unready(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug(f'Command /unready is triggered by {update.effective_user}')
    unready_message: ReadyMessage = ReadyMessage.from_resolved(
        ResolvedMessage.from_list(context.args)
    )
    user = update.effective_user.name

    await set_unready(user, unready_message, context)


async def set_ready(user: str, message: ReadyMessage, context: ContextTypes.DEFAULT_TYPE) -> None:
    day = message.day
    game = message.game
    ready_time = ReadyTime(message.ready_from, message.ready_until, UNTIL)
    context.chat_data[day][game][user] = ready_time
    logger.info(f'Success: user {user} is ready for {game} on {day} from {ready_time.since} to {ready_time.until}')


async def set_unready(user: str, message: ReadyMessage, context: ContextTypes.DEFAULT_TYPE) -> None:
    games = context.chat_data.get(message.day)
    if games:
        for game in games:
            if not message.game or game == message.game:
                context.chat_data[message.day][game].pop(user, None)
                logger.info(f'Success: user {user} is now NOT ready for {game} on {message.day}')
