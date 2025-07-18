import logging

from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import ColorNames, ColorSuits


class ColorDeck(BaseDeck):
    def __init__(self, is_shuffle: bool = True, total_decks: int = 1):
        quantities = {
            (ColorNames.ZERO, ColorSuits.BLACK): 0,
            (ColorNames.PLUS_ZERO, ColorSuits.BLACK): 4,
            (ColorNames.PLUS_FOUR, ColorSuits.BLACK): 4,
            ColorNames.ZERO: 1,
            ColorNames.PLUS_ZERO: 0,
            ColorNames.PLUS_FOUR: 0,
            ColorSuits.RED: 2,
            ColorSuits.BLUE: 2,
            ColorSuits.GREEN: 2,
            ColorSuits.YELLOW: 2,
            ColorSuits.BLACK: 0,
        }
        super().__init__(
            names=ColorNames,
            suits=ColorSuits,
            quantities=quantities,
            is_shuffle=is_shuffle,
            total_decks=total_decks,
        )


if __name__ == '__main__':
    deck = ColorDeck(is_shuffle=False, total_decks=1)
    logging.debug(len(deck))
    logging.debug(deck)
