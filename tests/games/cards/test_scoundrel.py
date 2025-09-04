import unittest

from bot.games.cards.scoundrel import ScoundrelCard
from bot.games.enums.card import RoyalNames, RoyalSuits


class TestScoundrelCard(unittest.TestCase):

    def setUp(self):
        self.ace_clubs = ScoundrelCard(RoyalNames.ACE, RoyalSuits.CLUBS)
        self.two_hearts = ScoundrelCard(RoyalNames.TWO, RoyalSuits.HEARTS)
        self.king_diamonds = ScoundrelCard(
            RoyalNames.KING,
            RoyalSuits.DIAMONDS
        )
        self.jack_spades = ScoundrelCard(RoyalNames.JACK, RoyalSuits.SPADES)
