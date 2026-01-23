import unittest

from bot.games.cards.nine_nine import NineNineCard
from bot.games.enums.card import NineNineNames, NineNineSuits


class TestNineNineCard(unittest.TestCase):

    def setUp(self):
        self.zero_card = NineNineCard(NineNineNames.ZERO, NineNineSuits.ORAGE)
        self.nine_nine_card = NineNineCard(
            NineNineNames.NINE_NINE, NineNineSuits.BLACK
        )
        self.reverse_card = NineNineCard(
            NineNineNames.REVERSE, NineNineSuits.GREEN
        )
        self.double_play_card = NineNineCard(
            NineNineNames.DOUBLE_PLAY, NineNineSuits.RED
        )
        self.number_card = NineNineCard(
            NineNineNames.FIVE, NineNineSuits.ORAGE
        )

    def test_zero_names_property(self):
        """Testa se zero_names property returna a tupla correta"""

        expected_zero_names = (
            NineNineNames.ZERO,
            NineNineNames.NINE_NINE,
            NineNineNames.REVERSE,
            NineNineNames.DOUBLE_PLAY,
        )
        self.assertEqual(self.zero_card.zero_names, expected_zero_names)

    def test_value_zero_names(self):
        """Testa se value property returna 0 para 'zero names'"""

        self.assertEqual(self.zero_card.value, 0)
        self.assertEqual(self.nine_nine_card.value, 0)
        self.assertEqual(self.reverse_card.value, 0)
        self.assertEqual(self.double_play_card.value, 0)

    def test_value_number_cards(self):
        """Testa se value property returna valores corretos para
        cartas de números.
        """

        test_cases = [
            (NineNineNames.ONE, 1),
            (NineNineNames.TWO, 2),
            (NineNineNames.THREE, 3),
            (NineNineNames.FOUR, 4),
            (NineNineNames.FIVE, 5),
            (NineNineNames.SIX, 6),
            (NineNineNames.SEVEN, 7),
            (NineNineNames.EIGHT, 8),
            (NineNineNames.NINE, 9),
            (NineNineNames.TEN, 10),
            (NineNineNames.MINUS_TEN, -10),
        ]

        for name, expected_value in test_cases:
            card = NineNineCard(name, NineNineSuits.ORAGE)
            self.assertEqual(card.value, expected_value)

    def test_suit_value(self):
        """Test suit_value property returns 1"""

        self.assertEqual(self.zero_card.suit_value, 1)
        self.assertEqual(self.number_card.suit_value, 1)
