"""
Бот сбора на игровое пати в Телеграм чате
"""

import html
import json
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler,
                          ContextTypes,
                          PicklePersistence,
                          filters)

from bot import config
import bot.handlers as handlers


config.configure_logging(logging.INFO)
logger = logging.getLogger('bot')


COMMAND_HANDLERS = {
    ('start', 'ready'): handlers.ready,
    'unready': handlers.unready,
    'party': handlers.party_command,
    'help': handlers.say_help
}

# CALLBACK_QUERY_HANDLERS = {
#     '^' f'{config.CALLBACK_PREFIX}(approve|decline)_[0-9]+' '$': handlers.process_button,
# }


def run_gameparty_bot():
    """Запускает бота @help_admin_1060_bot
    """
    app = ApplicationBuilder().token(
        config.ECHO_TOKEN if config.APP_ENV == 'dev' else config.BOT_TOKEN
    ).persistence(
        PicklePersistence(config.WORKDIR / config.PERSISTENCE_FILE, update_interval=60)
    ).build()

    logger.debug('App created')
    for command_name, command_handler in COMMAND_HANDLERS.items():
        app.add_handler(CommandHandler(command_name, command_handler))

    app.add_handler(CallbackQueryHandler(handlers.process_button))

    # for pattern, handler in CALLBACK_QUERY_HANDLERS.items():
    #     app.add_handler(CallbackQueryHandler(handler, pattern=pattern))

    if config.APP_ENV == 'dev':
        app.add_handler(MessageHandler(filters.TEXT, echo))
        app.add_handler(CallbackQueryHandler(callback_query_echo))
    elif config.APP_ENV == 'prod':
        app.add_handler(MessageHandler(filters.TEXT, log_missing))
        app.add_handler(CallbackQueryHandler(log_missing))

    app.add_error_handler(handlers.error_handler)

    app.run_polling()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "Это сообщение означает, что бот что-то не отловил:\n\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.bot_data = {html.escape(str(context.chat_data))}</pre>\n\n"
    )

    await context.bot.send_message(
        chat_id=config.SUPERUSER_ID,
        text=message,
        parse_mode=ParseMode.HTML
    )


async def callback_query_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer('Эта кнопка не активна')
    text = [
        'Эт сообщение означает, что нажатая кнопка не прошла ни один установленный фильтр.',
        '',
        'Нажата кнопка с параметром',
        f'<code>{query.data}</code>'
    ]
    text = '\n'.join(text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML
    )


async def log_missing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    text = [
        "Something happened and bot missed it:\n",
        " " * 76,
        f"update = {str(update_str)}\n",
        " " * 76,
        f"context.bot_data = {str(context.chat_data)}\n",
    ]
    text = "".join(text)
    logger.warning(text)


if __name__ == '__main__':
    run_gameparty_bot()
