from enum import Enum
import re
from typing import List, Union
from bot.functions.enumeration import get_enum_index
from bot.games.enums.card import (
    WILD_SUITS,
    ColorNames,
    FlipColorNames,
    FullRoyalNames,
    Names,
    RoyalNames,
    SpanishNames,
    StrippedSpanishNames,
    Suits
)


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

    def __gt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'Espera um {self.__class__.__name__}, '
                f'obteve {type(other)}({other})'
            )
        if self.value == other.value:
            return self.suit_value > other.suit_value
        else:
            return self.value > other.value

    def __hash__(self) -> int:
        return hash((self.name, self.suit))

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.__class__.__name__}({self.text})'

    def equals_name(self, other: Union['Card', Names]) -> bool:
        if isinstance(other, Names):
            return self.name == other
        elif isinstance(other, Card):
            return self.name == other.name
        else:
            return False

    def equals_suit(self, other: Union['Card', Suits]) -> bool:
        if isinstance(other, Suits):
            return self.suit == other
        elif isinstance(other, Card):
            return self.suit == other.suit
        else:
            return False

    def set_wild(self, name: Names, suit: Suits):
        self.set_wild_name(name)
        self.set_wild_suit(suit)

    def set_wild_name(self, name: Names):
        if not self.is_wild:
            raise ValueError(f'{self.suit.name} não é um valor WILD válido.')
        if not isinstance(name, self.name.__class__):
            raise TypeError(
                f'name precisa ser um Enum do tipo {self.name.__class__}.'
            )
        self.wild_name = name

    def set_wild_suit(self, suit: Suits):
        if not self.is_wild:
            raise ValueError(f'{self.suit.name} não é um valor WILD válido.')
        if not isinstance(suit, self.suit.__class__):
            raise TypeError(
                f'suit precisa ser um Enum do tipo {self.suit.__class__}.'
            )
        self.wild_suit = suit

    def unset_wild(self):
        self.wild_name = None
        self.wild_suit = None

    @property
    def text(self):
        return f'{self.suit.value}{self.name.value}'

    @property
    def value(self):
        return get_enum_index(self.name)

    @property
    def suit_value(self):
        return get_enum_index(self.suit)

    @property
    def plus_value(self) -> int:
        value_text = self.name.value
        plus_match = re.search(r'\+(\d+)', value_text)
        if plus_match:
            return int(plus_match.group(1))
        return 0

    @property
    def name(self):
        return self.wild_name if self.wild_name is not None else self.real_name

    @property
    def suit(self):
        return self.wild_suit if self.wild_suit is not None else self.real_suit

    @property
    def wild_terms(self) -> str:
        return '|'.join((suit.name for suit in WILD_SUITS))

    @property
    def is_wild(self) -> bool:
        return bool(re.search(self.wild_terms, self.suit.name, re.I))

    @property
    def number_card_names(self) -> List[Enum]:
        if isinstance(self.name, RoyalNames):
            return [
                RoyalNames.TWO, RoyalNames.THREE, RoyalNames.FOUR,
                RoyalNames.FIVE, RoyalNames.SIX, RoyalNames.SEVEN,
                RoyalNames.EIGHT, RoyalNames.NINE, RoyalNames.TEN
            ]
        elif isinstance(self.name, FullRoyalNames):
            return [
                FullRoyalNames.TWO, FullRoyalNames.THREE, FullRoyalNames.FOUR,
                FullRoyalNames.FIVE, FullRoyalNames.SIX, FullRoyalNames.SEVEN,
                FullRoyalNames.EIGHT, FullRoyalNames.NINE, FullRoyalNames.TEN
            ]
        elif isinstance(self.name, SpanishNames):
            return [
                SpanishNames.ONE, SpanishNames.TWO, SpanishNames.THREE,
                SpanishNames.FOUR, SpanishNames.FIVE, SpanishNames.SIX,
                SpanishNames.SEVEN, SpanishNames.EIGHT, SpanishNames.NINE,
                SpanishNames.KNAVE, SpanishNames.KNIGHT, SpanishNames.KING
            ]
        elif isinstance(self.name, StrippedSpanishNames):
            return [
                StrippedSpanishNames.ONE, StrippedSpanishNames.TWO,
                StrippedSpanishNames.THREE, StrippedSpanishNames.FOUR,
                StrippedSpanishNames.FIVE, StrippedSpanishNames.SIX,
                StrippedSpanishNames.SEVEN, StrippedSpanishNames.KNAVE,
                StrippedSpanishNames.KNIGHT, StrippedSpanishNames.KING
            ]
        elif isinstance(self.name, ColorNames):
            return [
                ColorNames.ZERO, ColorNames.ONE, ColorNames.TWO,
                ColorNames.THREE, ColorNames.FOUR, ColorNames.FIVE,
                ColorNames.SIX, ColorNames.SEVEN, ColorNames.EIGHT,
                ColorNames.NINE,
            ]
        elif isinstance(self.name, FlipColorNames):
            return [
                FlipColorNames.ZERO, FlipColorNames.ONE, FlipColorNames.TWO,
                FlipColorNames.THREE, FlipColorNames.FOUR, FlipColorNames.FIVE,
                FlipColorNames.SIX, FlipColorNames.SEVEN, FlipColorNames.EIGHT,
                FlipColorNames.NINE,
            ]
        else:
            raise ValueError(
                f'Não foi possível encontrar os números de {self.name}.'
            )

    @property
    def figure_card_names(self) -> List[Enum]:
        if isinstance(self.name, RoyalNames):
            return [RoyalNames.JACK, RoyalNames.QUEEN, RoyalNames.KING]
        elif isinstance(self.name, FullRoyalNames):
            return [
                FullRoyalNames.JACK, FullRoyalNames.QUEEN, FullRoyalNames.KING
            ]
        elif isinstance(self.name, SpanishNames):
            return [SpanishNames.KNAVE, SpanishNames.KNIGHT, SpanishNames.KING]
        elif isinstance(self.name, StrippedSpanishNames):
            return [
                StrippedSpanishNames.KNAVE, StrippedSpanishNames.KNIGHT,
                StrippedSpanishNames.KING
            ]
        elif isinstance(self.name, ColorNames):
            return []
        elif isinstance(self.name, FlipColorNames):
            return []
        else:
            raise ValueError(
                f'Não foi possível encontrar os números de {self.name}.'
            )

    @property
    def special_card_names(self) -> List[Enum]:
        if isinstance(self.name, RoyalNames):
            return [RoyalNames.ACE]
        elif isinstance(self.name, FullRoyalNames):
            return [FullRoyalNames.ACE]
        elif isinstance(self.name, SpanishNames):
            return []
        elif isinstance(self.name, StrippedSpanishNames):
            return []
        elif isinstance(self.name, ColorNames):
            return []
        elif isinstance(self.name, FlipColorNames):
            return []
        else:
            raise ValueError(
                f'Não foi possível encontrar os números de {self.name}.'
            )

    @property
    def extra_card_names(self) -> List[Enum]:
        if isinstance(self.name, RoyalNames):
            return []
        elif isinstance(self.name, FullRoyalNames):
            return [FullRoyalNames.JOKER]
        elif isinstance(self.name, SpanishNames):
            return []
        elif isinstance(self.name, StrippedSpanishNames):
            return []
        elif isinstance(self.name, ColorNames):
            return []
        elif isinstance(self.name, FlipColorNames):
            return []
        else:
            raise ValueError(
                f'Não foi possível encontrar os números de {self.name}.'
            )

    @property
    def action_card_names(self) -> List[Enum]:
        if isinstance(self.name, RoyalNames):
            return []
        elif isinstance(self.name, FullRoyalNames):
            return []
        elif isinstance(self.name, SpanishNames):
            return []
        elif isinstance(self.name, StrippedSpanishNames):
            return []
        elif isinstance(self.name, ColorNames):
            return [
                ColorNames.BLOCK, ColorNames.REVERSE,
                ColorNames.PLUS_TWO, ColorNames.PLUS_FOUR
            ]
        elif isinstance(self.name, FlipColorNames):
            return [
                FlipColorNames.BLOCK_ALL, FlipColorNames.REVERSE,
                FlipColorNames.PLUS_FIVE, FlipColorNames.PLUS_COLOR
            ]
        else:
            raise ValueError(
                f'Não foi possível encontrar os números de {self.name}.'
            )
