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
        if not isinstance(other, (Card, Names)):
            return False
        elif isinstance(other, Names):
            return self.name == other
        elif isinstance(other, Card):
            return self.name == other.name
        else:
            raise TypeError('Não deveria entrar aqui.')

    def equals_suit(self, other) -> bool:
        if not isinstance(other, (Card, Suits)):
            return False
        elif isinstance(other, Suits):
            return self.suit == other
        elif isinstance(other, Card):
            return self.suit == other.suit
        else:
            raise TypeError('Não deveria entrar aqui.')

    @property
    def text(self):
        return f'{self.suit.value}{self.name.value}'

    @property
    def value(self):
        return get_enum_index(self.name)
