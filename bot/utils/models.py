import logging
from datetime import date, timedelta
from dataclasses import dataclass, field, InitVar

from bot.config import (aliases, DEFAULT, configure_logging, NOT_RESOLVED, TIMESTAMP, PLUS, MINUS,
                        GAME, DAY, WEEKDAY, TIME, NUMERALS, OTHER,
                        FROM, UNTIL, AT, FOR, HOUR, HOURS)


logger = logging.getLogger(__name__)


@dataclass
class ResolvedMessage:
    game: str = None
    day: int = None
    weekday: int = None
    time: int = None
    ready_from: int = None
    ready_until: int = None
    ready_at: int = None
    ready_for: int = None
    not_resolved: list[str] = field(default_factory=list)

    @classmethod
    def from_list(cls, args: list[str]) -> 'ResolvedMessage':
        logger.debug(f'Resolving: {args}')
        message = cls()

        i = 0
        while i < len(args):
            key, value = _resolve(args[i])
            if key == NOT_RESOLVED:
                message.not_resolved.append(value)
            elif key == OTHER and value in (FOR, HOUR, HOURS):
                # TODO сделать распознавание сообщения вида 'на 4 часа'
                # i += 1
                # next_arg = args[i]
                # if next_arg in aliases[OTHER][HOUR]:
                #
                # numeral = _resolve_numeral(args[i + 1])
                # if numeral:
                message.not_resolved.append(args[i])

            elif key == OTHER and value in (FROM, UNTIL, AT):
                i += 1
                next_key, next_value = _resolve(args[i])
                if next_key == TIME:
                    message.__dict__[value] = next_value
            else:
                message.__dict__[key] = value
            i += 1
        logger.info(f'Resolved {message} from {args}')
        return message


@dataclass
class ReadyMessage:
    game: str
    day: str
    ready_from: int = None
    ready_until: int = None

    def __post_init__(self):
        if not self.ready_from:
            self.ready_from = DEFAULT['ready_from']
        if not self.ready_until:
            self.ready_until = DEFAULT['ready_until']

    @classmethod
    def from_resolved(cls, message: ResolvedMessage) -> 'ReadyMessage':
        ready_from = message.ready_from if message.ready_from else message.ready_at
        ready_until = message.ready_until
        if not ready_until and ready_from and message.ready_for:
            ready_until = ready_from + message.ready_for
        ready_message = cls(game=message.game if message.game else DEFAULT['game'],
                            day=_make_datestr(message),
                            ready_from=ready_from,
                            ready_until=ready_until)

        logger.info(f'Created {ready_message} from {message}')
        return ready_message


@dataclass
class ReadyTime:
    since: int
    until: int
    changing: str

    def __post_init__(self):
        self.validate_time()

    def update(self, action: str) -> None:
        if action == PLUS:
            self.__dict__[self.changing] += 1
        elif action == MINUS:
            self.__dict__[self.changing] -= 1
        else:
            logger.error(f'Invalid action: {action}')

        self.validate_time(action)

    def validate_time(self, action: str = PLUS) -> None:
        self.since = self.since % 24
        self.until = self.until % 24

        if self.changing == FROM and action == PLUS and self.until == self.since:
            self.until = self.since + 1
        elif self.changing == UNTIL and action == MINUS and self.until == self.since:
            self.since = self.until - 1


def _resolve(alias) -> tuple:
    result = (NOT_RESOLVED, alias)
    for key, values in aliases.items():
        for value, alias_list in values.items():
            if alias in alias_list:
                if key in (DAY, WEEKDAY, TIME, NUMERALS):
                    value = int(value)
                result = (key, value)
    return result


def _resolve_numeral(alias) -> tuple:
    for key, values in NUMERALS.items():
        if alias in values:
            return key


def _make_datestr(message: ResolvedMessage) -> str:
    if message.day is not None:
        day = _make_datestr_from_number(message.day)
    elif message.weekday:
        day = _make_datestr_from_number(message.weekday, True)
    else:
        day = _make_datestr_from_number(DEFAULT['day'])
    return day


def _make_datestr_from_number(days: int, weekdays_mode: bool = False) -> str:
    if weekdays_mode:
        return _make_datestr_from_number((days - date.today().weekday() + 7) % 7)
    return (date.today() + timedelta(days=days)).strftime(TIMESTAMP)


if __name__ == '__main__':
    configure_logging(logging.DEBUG)
    from_args = ['кс', 'до', '23', 'часа', 'сегодня', 'с', '18', 'пятница']

    ReadyMessage.from_resolved(ResolvedMessage.from_list(from_args))
