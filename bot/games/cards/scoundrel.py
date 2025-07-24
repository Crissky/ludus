from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits


class ScoundrelCard(Card):
    @property
    def value(self):
        if self.name == RoyalNames.ACE:
            return 14
        else:
            return super().value + 1

    @property
    def suit_value(self):
        return 1

    @property
    def is_weapon(self):
        return self.suit in [RoyalSuits.DIAMONDS]

    @property
    def is_potion(self):
        return self.suit in [RoyalSuits.HEARTS]

    @property
    def is_enemy(self):
        return self.suit in [RoyalSuits.CLUBS, RoyalSuits.SPADES]
