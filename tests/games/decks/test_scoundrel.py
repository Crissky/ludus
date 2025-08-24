import unittest

from bot.games.cards.scoundrel import ScoundrelCard
from bot.games.decks.scoundrel import ScoundrelDeck
from bot.games.enums.card import RoyalNames, RoyalSuits


class TestScoundrelDeck(unittest.TestCase):
    def test_init_default(self):
        """Teste inicialização padrão do ScoundrelDeck."""

        deck = ScoundrelDeck(is_shuffle=False)

        self.assertEqual(len(deck), 44)
        self.assertEqual(deck.card_class, ScoundrelCard)

    def test_excluded_cards(self):
        """Teste se as cartas corretas foram excluídas."""

        deck = ScoundrelDeck(is_shuffle=False)

        excluded_cards = [
            (RoyalNames.ACE, RoyalSuits.DIAMONDS),
            (RoyalNames.ACE, RoyalSuits.HEARTS),
            (RoyalNames.JACK, RoyalSuits.DIAMONDS),
            (RoyalNames.JACK, RoyalSuits.HEARTS),
            (RoyalNames.QUEEN, RoyalSuits.DIAMONDS),
            (RoyalNames.QUEEN, RoyalSuits.HEARTS),
            (RoyalNames.KING, RoyalSuits.DIAMONDS),
            (RoyalNames.KING, RoyalSuits.HEARTS),
        ]

        deck_cards = [(card.name, card.suit) for card in deck]
        for name, suit in excluded_cards:
            self.assertNotIn((name, suit), deck_cards)

    def test_multiple_decks(self):
        """Teste inicialização com múltiplos baralhos."""

        deck = ScoundrelDeck(is_shuffle=False, total_decks=2)

        self.assertEqual(len(deck), 88)

    def test_count_suits(self):
        """Teste contagem de naipes."""

        deck = ScoundrelDeck(is_shuffle=False)
        suit_dict = {suit: 0 for suit in RoyalSuits}
        red_suit_list = [RoyalSuits.DIAMONDS, RoyalSuits.HEARTS]
        for card in deck:
            suit = card.suit
            suit_dict[suit] += 1

        for suit, value in suit_dict.items():
            if suit in red_suit_list:
                self.assertEqual(value, 9)
            else:
                self.assertEqual(value, 13)

    def test_count_names(self):
        """Teste contagem de nomes."""

        deck = ScoundrelDeck(is_shuffle=False)
        name_dict = {name: 0 for name in RoyalNames}
        for card in deck:
            name = card.name
            name_dict[name] += 1

        for name, value in name_dict.items():
            only_black_names = [
                RoyalNames.ACE,
                RoyalNames.JACK,
                RoyalNames.QUEEN,
                RoyalNames.KING
            ]
            if name in only_black_names:
                self.assertEqual(value, 2)
            else:
                self.assertEqual(value, 4)
