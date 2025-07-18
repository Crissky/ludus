import logging

from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import RoyalNames, RoyalSuits


class RoyalDeck(BaseDeck):
    def __init__(self, is_shuffle: bool = True, total_decks: int = 1):
        super().__init__(
            names=RoyalNames,
            suits=RoyalSuits,
            is_shuffle=is_shuffle,
            total_decks=total_decks,
        )


if __name__ == '__main__':
    deck = RoyalDeck(is_shuffle=False, total_decks=1)
    logging.debug(len(deck))
    logging.debug(deck)
