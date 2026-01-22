from typing import Tuple
from bot.games.cards.card import Card
from bot.games.enums.card import NineNineNames


class NineNineCard(Card):

    @property
    def zero_names(self) -> Tuple[NineNineNames]:
        return (
            NineNineNames.ZERO,
            NineNineNames.NINE_NINE,
            NineNineNames.REVERSE,
            NineNineNames.DOUBLE_PLAY,
        )

    @property
    def value(self) -> int:
        result = 0
        if self.name in self.zero_names:
            result = 0
        elif self.name == NineNineNames.ONE:
            result = 1
        elif self.name == NineNineNames.TWO:
            result = 2
        elif self.name == NineNineNames.THREE:
            result = 3
        elif self.name == NineNineNames.FOUR:
            result = 4
        elif self.name == NineNineNames.FIVE:
            result = 5
        elif self.name == NineNineNames.SIX:
            result = 6
        elif self.name == NineNineNames.SEVEN:
            result = 7
        elif self.name == NineNineNames.EIGHT:
            result = 8
        elif self.name == NineNineNames.NINE:
            result = 9
        elif self.name == NineNineNames.TEN:
            result = 10
        elif self.name == NineNineNames.MINUS_TEN:
            result = -10

        return result

    @property
    def suit_value(self):
        return 1
