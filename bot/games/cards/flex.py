import logging

from typing import Union

from bot.games.cards.card import Card
from bot.games.enums.card import Names, Suits


class FlexCard(Card):
    def __init__(
        self,
        name: Names,
        suit: Suits,
        flex: Union[Names, Suits] = None
    ):
        super().__init__(name, suit)

        if not isinstance(flex, (Names, Suits, type(None))):
            raise TypeError(
                'flex precisa ser um Enum do tipo Names ou Suits (ou None).'
            )
        self.flex = flex

    def __eq__(self, other):
        if hasattr(other, 'flex'):
            return super().__eq__(other) and self.flex == other.flex
        return False

    def __hash__(self) -> int:
        return hash((self.name, self.suit, self.flex))

    def equals_name(self, other: Union[Card, Names]) -> bool:
        if isinstance(other, Names):
            return self.name == other or self.flex == other
        elif isinstance(other, Card):
            return self.name == other.name or self.flex == other.name
        else:
            return False

    def equals_suit(self, other: Union[Card, Suits]) -> bool:
        if isinstance(other, Suits):
            return self.suit == other or self.flex == other
        elif isinstance(other, Card):
            return self.suit == other.suit or self.flex == other.suit
        else:
            return False

    @property
    def text(self):
        if self.flex is None:
            return super().text
        return f'{self.suit.value}{self.name.value}({self.flex.value})'


if __name__ == '__main__':
    from bot.games.enums.card import ColorNames, ColorSuits
    card = FlexCard(ColorNames.SEVEN, ColorSuits.RED, ColorSuits.BLUE)
    logging.debug('Text:', card.text)
    logging.debug('Name:', card.name)
    logging.debug('Suit:', card.suit)
    logging.debug('Flex:', card.flex)
    card = FlexCard(ColorNames.REVERSE, ColorSuits.RED, ColorNames.BLOCK)
    logging.debug('Text:', card.text)
    logging.debug('Name:', card.name)
    logging.debug('Suit:', card.suit)
    logging.debug('Flex:', card.flex)
