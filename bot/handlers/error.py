import html
import json
import traceback
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import config

logger = logging.getLogger(__name__)


def class_to_dict(obj) -> dict:
    return obj.__dict__


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message_with_update = (
        'An exception was raised while handling an update\n\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>'
    )
    message_with_context = (
        f'<pre language="python">context.chat_data = '
        f'{html.escape(json.dumps(context.chat_data, indent=2, ensure_ascii=False, default=class_to_dict))}'
        f'</pre>'
    )
    message_with_traceback = f'<pre language="python">{html.escape(tb_string)}</pre>'

    # Finally, send the message
    await context.bot.send_message(
        chat_id=config.SUPERUSER_ID, text=message_with_update, parse_mode=ParseMode.HTML
    )
    await context.bot.send_message(
        chat_id=config.SUPERUSER_ID, text=message_with_context, parse_mode=ParseMode.HTML
    )
    await context.bot.send_message(
        chat_id=config.SUPERUSER_ID, text=message_with_traceback, parse_mode=ParseMode.HTML
    )
