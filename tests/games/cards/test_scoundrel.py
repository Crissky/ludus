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

    def test_value_non_ace(self):
        """Teste se cartas não-ACE retornam valor base + 1."""

        self.assertEqual(self.two_clubs.value, 2)
        self.assertEqual(self.two_diamonds.value, 2)
        self.assertEqual(self.two_hearts.value, 2)
        self.assertEqual(self.two_spades.value, 2)

        self.assertEqual(self.jack_clubs.value, 11)
        self.assertEqual(self.jack_diamonds.value, 11)
        self.assertEqual(self.jack_hearts.value, 11)
        self.assertEqual(self.jack_spades.value, 11)

        self.assertEqual(self.king_clubs.value, 13)
        self.assertEqual(self.king_diamonds.value, 13)
        self.assertEqual(self.king_hearts.value, 13)
        self.assertEqual(self.king_spades.value, 13)

    def test_suit_value(self):
        """Teste se suit_value sempre retorna 1."""

        self.assertEqual(self.ace_clubs.suit_value, 1)
        self.assertEqual(self.ace_diamonds.suit_value, 1)
        self.assertEqual(self.ace_hearts.suit_value, 1)
        self.assertEqual(self.ace_spades.suit_value, 1)

        self.assertEqual(self.two_clubs.suit_value, 1)
        self.assertEqual(self.two_diamonds.suit_value, 1)
        self.assertEqual(self.two_hearts.suit_value, 1)
        self.assertEqual(self.two_spades.suit_value, 1)

        self.assertEqual(self.king_clubs.suit_value, 1)
        self.assertEqual(self.king_diamonds.suit_value, 1)
        self.assertEqual(self.king_hearts.suit_value, 1)
        self.assertEqual(self.king_spades.suit_value, 1)

    def test_is_weapon_diamonds(self):
        """Teste se DIAMONDS é arma."""

        self.assertTrue(self.ace_diamonds.is_weapon)
        self.assertTrue(self.two_diamonds.is_weapon)
        self.assertTrue(self.jack_diamonds.is_weapon)
        self.assertTrue(self.king_diamonds.is_weapon)

    def test_is_weapon_non_diamonds(self):
        """Teste se outros naipes não são armas."""

        self.assertFalse(self.ace_clubs.is_weapon)
        self.assertFalse(self.ace_hearts.is_weapon)
        self.assertFalse(self.ace_spades.is_weapon)
        self.assertFalse(self.two_clubs.is_weapon)
        self.assertFalse(self.two_hearts.is_weapon)
        self.assertFalse(self.two_spades.is_weapon)
        self.assertFalse(self.jack_clubs.is_weapon)
        self.assertFalse(self.jack_hearts.is_weapon)
        self.assertFalse(self.jack_spades.is_weapon)
        self.assertFalse(self.king_clubs.is_weapon)
        self.assertFalse(self.king_hearts.is_weapon)
        self.assertFalse(self.king_spades.is_weapon)
