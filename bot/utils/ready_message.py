import logging
from datetime import date, timedelta
from dataclasses import dataclass, field, InitVar

from bot.config import (aliases, default_ready, configure_logging,
                        NOT_RESOLVED, DAY, WEEKDAY, HOURS, READY_FROM, IGNORED, TIMESTAMP, AMOUNTS)


logger = logging.getLogger(__name__)


@dataclass
class ResolvedMessage:
    game: str = None
    day: int = None
    weekday: int = None
    hours: int = None
    ready_from: int = None
    not_resolved: list[str] = field(default_factory=list)

    @classmethod
    def from_list(cls, args: list[str]) -> 'ResolvedMessage':
        logger.debug(f'Resolving: {args}')
        message = cls()
        for i, arg in enumerate(args):
            if arg in IGNORED:
                continue
            elif arg in AMOUNTS:
                arg += ' ' + args[i + 1]
            key, value = _resolve(arg)
            if key == NOT_RESOLVED:
                message.not_resolved.append(value)
            else:
                message.__dict__[key] = value
        logger.info(f'Resolved {message} from {args}')
        return message


@dataclass
class ReadyMessage:
    game: str
    day: str
    hours: InitVar[int] = 0
    ready_from: InitVar[int] = 0
    ready_hours: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self, hours: int, ready_from: int):
        self.ready_hours = {hour: False for hour in aliases['ready_from'].keys()}
        if hours and ready_from:
            for hour in range(ready_from, ready_from + hours):
                if hour > 23:
                    break
                self.ready_hours[str(hour)] = True

    @classmethod
    def from_resolved(cls, message: ResolvedMessage) -> 'ReadyMessage':
        if message.day is not None:
            day = _make_datestr_from(message.day)
        elif message.weekday:
            day = _make_datestr_from(message.weekday, True)
        else:
            day = _make_datestr_from(default_ready['day'])
        ready_message = cls(game=message.game if message.game else default_ready['game'],
                            day=day,
                            hours=message.hours if message.hours else default_ready['hours'],
                            ready_from=message.ready_from if message.ready_from else default_ready['ready_from'])

        logger.info(f'Created {ready_message} from {message}')
        return ready_message


def _resolve(alias) -> tuple:
    result = (NOT_RESOLVED, alias)
    for key, values in aliases.items():
        for value, alias_list in values.items():
            if alias in alias_list:
                if key in (DAY, WEEKDAY, HOURS, READY_FROM):
                    value = int(value)
                result = (key, value)
    return result


def _make_datestr_from(days: int, weekdays_mode: bool = False) -> str:
    if weekdays_mode:
        return _make_datestr_from((days - date.today().weekday() + 7) % 7)
    return (date.today() + timedelta(days=days)).strftime(TIMESTAMP)
