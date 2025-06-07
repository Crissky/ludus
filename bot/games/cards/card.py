import re
from bot.functions.enumeration import get_enum_index
from bot.games.enums.card import WILD_SUITS, Names, Suits


class Card:
    def __init__(self, name: Names, suit: Suits):
        if not isinstance(name, Names):
            raise TypeError('name precisa ser um Enum do tipo Names.')
        if not isinstance(suit, Suits):
            raise TypeError('suit precisa ser um Enum do tipo Suits.')

        self.real_name = name
        self.real_suit = suit
        self.wild_name = None
        self.wild_suit = None

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

    def set_wild(self, name: Names, suit: Suits):
        self.set_wild_name(name)
        self.set_wild_suit(suit)

    def set_wild_name(self, name: Names):
        if not re.search(self.wild_terms, self.suit.name, re.I):
            raise ValueError(f'{self.suit.name} não é um valor WILD válido.')
        if not isinstance(name, self.name.__class__):
            raise TypeError(
                f'name precisa ser um Enum do tipo {self.name.__class__}.'
            )
        self.wild_name = name

    def set_wild_suit(self, suit: Suits):
        if not re.search(self.wild_terms, self.suit.name, re.I):
            raise ValueError(f'{self.suit.name} não é um valor WILD válido.')
        if not isinstance(suit, self.suit.__class__):
            raise TypeError(
                f'suit precisa ser um Enum do tipo {self.suit.__class__}.'
            )
        self.wild_suit = suit

    @property
    def text(self):
        return f'{self.suit.value}{self.name.value}'

    @property
    def value(self):
        return get_enum_index(self.name)

    @property
    def name(self):
        return self.wild_name if self.wild_name is not None else self.real_name

    @property
    def suit(self):
        return self.wild_suit if self.wild_suit is not None else self.real_suit

    @property
    def wild_terms(self) -> str:
        return '|'.join((suit.name for suit in WILD_SUITS))
