from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames


class ScoundrelCard(Card):
    @property
    def value(self):
        if self.name == RoyalNames.ACE:
            return 14
        else:
            return super().value

    @property
    def suit_value(self):
        return 1
