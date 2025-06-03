from bot.functions.enumeration import get_enum_index
from bot.games.enums.card import Names, Suits


class Card:
    def __init__(self, name: Names, suit: Suits):
        if not isinstance(name, Names):
            raise TypeError('name precisa ser um Enum do tipo Names.')
        if not isinstance(suit, Suits):
            raise TypeError('suit precisa ser um Enum do tipo Suits.')

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
