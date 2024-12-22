from telegram.ext import ContextTypes
from telegram import User


def log_entry_with_several_lines(user: User, game: str, day: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    users = context.chat_data[day][game]
    text = f'Showing `{game}` party on `{day}` to {user}'
    for user, ready_time in users.items():
        text += '\n'
        text += f'{" " * 76}{user}: '
        text += ' '.join([f'{key}={value}' for key, value in ready_time.__dict__.items()])

    return text
