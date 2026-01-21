import logging

from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import NineNineNames, NineNineSuits


class NienNineDeck(BaseDeck):
    def __init__(self, is_shuffle: bool = True, total_decks: int = 1):
        quantities = {
            (NineNineNames.ZERO, NineNineSuits.ORAGE): 8,
            (NineNineNames.TEN, NineNineSuits.ORAGE): 10,
            (NineNineNames.NINE_NINE, NineNineSuits.ORAGE): 0,
            (NineNineNames.REVERSE, NineNineSuits.ORAGE): 0,
            (NineNineNames.DOUBLE_PLAY, NineNineSuits.ORAGE): 0,
            (NineNineNames.MINUS_TEN, NineNineSuits.ORAGE): 0,
            (NineNineNames.REVERSE, NineNineSuits.GREEN): 10,
            (NineNineNames.DOUBLE_PLAY, NineNineSuits.RED): 10,
            (NineNineNames.MINUS_TEN, NineNineSuits.BLUE): 10,
            (NineNineNames.NINE_NINE, NineNineSuits.BLACK): 10,
            NineNineSuits.ORAGE: 6,
            NineNineSuits.GREEN: 0,
            NineNineSuits.RED: 0,
            NineNineSuits.BLUE: 0,
            NineNineSuits.BLACK: 0,
        }
        super().__init__(
            names=NineNineNames,
            suits=NineNineSuits,
            quantities=quantities,
            is_shuffle=is_shuffle,
            total_decks=total_decks,
        )


if __name__ == "__main__":
    from collections import Counter

    deck = NienNineDeck(is_shuffle=False, total_decks=1)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.debug(len(deck))
    logging.debug(f"Possui 112 cartas? {len(deck) == 112}")
    for card in (count := Counter(deck)):
        logging.debug((card, count[card]))
    logging.debug(deck)
