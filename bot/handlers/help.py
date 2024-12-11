import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


async def say_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug(f'Help is triggered by {update.effective_user}')
    text = (
        'Привет!\n'
        'Я помогаю собрать пати в чате\n'
        '\n'
        '<b>Доступные команды:</b>\n'
        '/ready - готов играть сегодня в CS2\n'
        '/unready - отменить готовность играть\n'
        '/party - посмотреть собранное пати\n'
        '\n'
        'Вместе с командами можно использовать слова, обозначающие день игры,'
        'время старта и длительность. Например:\n'
        '\n'
        '<code>/ready кс с 9 на пару часиков</code>\n'
        '<code>/ready послезавтра с 19 на 3 часа</code>\n'
        '<code>/unready в четверг</code>\n'
        '<code>/party завтра</code>\n'
    )
    await context.bot.send_message(
        update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML
    )
