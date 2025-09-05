import unittest

from bot.games.cards.scoundrel import ScoundrelCard
from bot.games.enums.card import RoyalNames, RoyalSuits


class TestScoundrelCard(unittest.TestCase):

    def setUp(self):
        self.ace_clubs = ScoundrelCard(RoyalNames.ACE, RoyalSuits.CLUBS)
        self.ace_diamonds = ScoundrelCard(RoyalNames.ACE, RoyalSuits.DIAMONDS)
        self.ace_hearts = ScoundrelCard(RoyalNames.ACE, RoyalSuits.HEARTS)
        self.ace_spades = ScoundrelCard(RoyalNames.ACE, RoyalSuits.SPADES)

        self.two_clubs = ScoundrelCard(RoyalNames.TWO, RoyalSuits.CLUBS)
        self.two_diamonds = ScoundrelCard(RoyalNames.TWO, RoyalSuits.DIAMONDS)
        self.two_hearts = ScoundrelCard(RoyalNames.TWO, RoyalSuits.HEARTS)
        self.two_spades = ScoundrelCard(RoyalNames.TWO, RoyalSuits.SPADES)

        self.king_clubs = ScoundrelCard(RoyalNames.KING, RoyalSuits.CLUBS)
        self.king_diamonds = ScoundrelCard(
            RoyalNames.KING,
            RoyalSuits.DIAMONDS
        )
        self.king_hearts = ScoundrelCard(RoyalNames.KING, RoyalSuits.HEARTS)
        self.king_spades = ScoundrelCard(RoyalNames.KING, RoyalSuits.SPADES)

        self.jack_clubs = ScoundrelCard(RoyalNames.JACK, RoyalSuits.CLUBS)
        self.jack_diamonds = ScoundrelCard(
            RoyalNames.JACK,
            RoyalSuits.DIAMONDS
        )
        self.jack_hearts = ScoundrelCard(RoyalNames.JACK, RoyalSuits.HEARTS)
        self.jack_spades = ScoundrelCard(RoyalNames.JACK, RoyalSuits.SPADES)

    def test_value_ace(self):
        """Teste se ACE retorna valor 14."""

        self.assertEqual(self.ace_clubs.value, 14)
        self.assertEqual(self.ace_diamonds.value, 14)
        self.assertEqual(self.ace_hearts.value, 14)
        self.assertEqual(self.ace_spades.value, 14)
