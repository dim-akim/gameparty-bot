from telegram.ext import ContextTypes


def log_entry_with_several_lines(game: str, day: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    users = context.chat_data[day][game]
    text = f'Showing `{game}` party on  `{day}`'
    for user, time_dict in users.items():
        text += '\n'
        text += f'{" " * 76}{user}: '
        text += ' '.join([f'{key}={value}' for key, value in time_dict.items()])

    return text
