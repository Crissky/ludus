from enum import Enum

from bot.functions.enumeration import get_enum_index


class Card:
    def __init__(self, name: Enum, suit: Enum):
        self.name = name
        self.suit = suit

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.__name__}({self.text})'

    @property
    def text(self):
        return f'{self.suit.value}{self.name.value}'

    @property
    def value(self):
        return get_enum_index(self.name)
