import logging

from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import RoyalNames, RoyalSuits


class RoyalDeck(BaseDeck):
    def __init__(self, shuffle: bool = True, total_decks: int = 1):
        super().__init__(
            names=RoyalNames,
            suits=RoyalSuits,
            shuffle=shuffle,
            total_decks=total_decks,
        )


if __name__ == '__main__':
    deck = RoyalDeck(shuffle=False, total_decks=2)
    logging.debug(len(deck))
    logging.debug(deck)
