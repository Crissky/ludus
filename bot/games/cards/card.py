from enum import Enum

from bot.functions.enumeration import get_enum_index


class Card:
    def __init__(self, name: Enum, suit: Enum):
        self.name = name
        self.suit = suit

    @property
    def text(self):
        return f'{self.suit.value}{self.name}'

    @property
    def value(self):
        return get_enum_index(self.name)
