import unittest

from bot.games.decks.royal import RoyalDeck
from bot.games.enums.card import RoyalNames, RoyalSuits


class TestRoyalDeck(unittest.TestCase):
    def test_init_default(self):
        """Teste inicialização padrão do RoyalDeck."""

        deck = RoyalDeck(is_shuffle=False)

        self.assertEqual(len(deck), 52)
        self.assertEqual(deck.names, RoyalNames)
        self.assertEqual(deck.suits, RoyalSuits)

    def test_init_multiple_decks(self):
        """Teste inicialização com múltiplos baralhos."""

        deck = RoyalDeck(is_shuffle=False, total_decks=2)

        self.assertEqual(len(deck), 104)

    def test_init_shuffled(self):
        """Teste se o embaralhamento funciona."""

        deck1 = RoyalDeck(is_shuffle=False)
        deck2 = RoyalDeck(is_shuffle=True)

        # Verifica se as ordens são diferentes (altamente provável)
        cards1 = [str(card) for card in deck1]
        cards2 = [str(card) for card in deck2]
        self.assertNotEqual(cards1, cards2)
        self.assertEqual(sorted(cards1), sorted(cards2))
