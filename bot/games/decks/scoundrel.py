import logging

from bot.games.cards.scoundrel import ScoundrelCard
from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import RoyalNames, RoyalSuits


class ScoundrelDeck(BaseDeck):
    def __init__(self, is_shuffle: bool = True, total_decks: int = 1):
        quantities = {
            (RoyalNames.ACE, RoyalSuits.DIAMONDS): 0,
            (RoyalNames.ACE, RoyalSuits.HEARTS): 0,
            (RoyalNames.JACK, RoyalSuits.DIAMONDS): 0,
            (RoyalNames.JACK, RoyalSuits.HEARTS): 0,
            (RoyalNames.QUEEN, RoyalSuits.DIAMONDS): 0,
            (RoyalNames.QUEEN, RoyalSuits.HEARTS): 0,
            (RoyalNames.KING, RoyalSuits.DIAMONDS): 0,
            (RoyalNames.KING, RoyalSuits.HEARTS): 0,
        }
        super().__init__(
            names=RoyalNames,
            suits=RoyalSuits,
            quantities=quantities,
            is_shuffle=is_shuffle,
            total_decks=total_decks,
            card_class=ScoundrelCard,
        )


if __name__ == '__main__':
    deck = ScoundrelDeck(is_shuffle=False, total_decks=1)
    # Configure logging with debug level, format and stream handler
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logging.debug(len(deck))
    logging.debug(f'Possui 44 cartas? {len(deck) == 44}')
    logging.debug(deck)
