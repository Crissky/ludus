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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.name == other.name and self.suit == other.suit

    def __hash__(self):
        return hash((self.name, self.suit))

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.__class__.__name__}({self.text})'

    def equals_name(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.name == other.name

    def equals_suit(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit

    @property
    def text(self):
        return f'{self.suit.value}{self.name.value}'

    @property
    def value(self):
        return get_enum_index(self.name)
