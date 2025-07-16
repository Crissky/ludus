import unittest

from bot.games.hands.hand import BaseHand
from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits


class TestHand(unittest.TestCase):
    def setUp(self):
        self.card1 = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        self.card2 = Card(RoyalNames.KING, RoyalSuits.HEARTS)
        self.card3 = Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)
        self.sample_cards = [self.card1, self.card2, self.card3]

    def test_init_empty(self):
        hand = BaseHand()
        self.assertEqual(len(hand), 0)
        self.assertEqual(hand.max_size, 0)

    def test_init_with_cards(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards, max_size=5)
        self.assertEqual(len(hand), 3)
        self.assertEqual(hand.max_size, 5)

    def test_getitem(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards)
        self.assertEqual(hand[0], sample_cards[0])

    def test_setitem(self):
        sample_cards = self.sample_cards
        hand = BaseHand(sample_cards[0])
        hand[0] = sample_cards[1]
        self.assertEqual(hand[0], sample_cards[1])

    def test_iter(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards)
        cards = list(hand)
        self.assertListEqual(cards, sample_cards)

    def test_len(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards)
        self.assertEqual(len(hand), 3)

    def test_str(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards)
        expected = ', '.join(card.text for card in sample_cards)
        self.assertEqual(str(hand), expected)

    def test_add_card_single(self):
        hand = BaseHand()
        card = self.card1
        hand.add_card(card)
        self.assertEqual(len(hand), 1)
        self.assertEqual(hand[0], card)

    def test_add_card_with_max_size(self):
        hand = BaseHand(max_size=2)
        cards = self.sample_cards

        discarded = hand.add_card(*cards)
        self.assertEqual(len(hand), 2)
        self.assertEqual(len(discarded), 1)

    def test_add_card_invalid_type(self):
        hand = BaseHand()
        msg_error = "Espera um Card, obteve <class 'str'>(not a card)"
        with self.assertRaises(TypeError) as context:
            hand.add_card("not a card")

        self.assertEqual(str(context.exception), msg_error)

    def test_discard(self):
        hand = BaseHand(self.card1)
        discarded = hand.discard()
        self.assertEqual(len(hand), 0)
        self.assertEqual(len(discarded), 1)
        self.assertIn(self.card1, discarded)

    def test_discard_empty_hand(self):
        hand = BaseHand()
        msg_error = "empty range for randrange() (0, 0, 0)"
        with self.assertRaises(ValueError) as context:
            hand.discard()

        self.assertEqual(str(context.exception), msg_error)

    def test_play(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards)
        played = hand.play(0, 2)
        self.assertEqual(len(hand), 1)
        self.assertEqual(len(played), 2)
        self.assertIn(self.card1, played)
        self.assertIn(self.card3, played)
        self.assertIn(self.card2, hand)

    def test_peek(self):
        sample_cards = self.sample_cards
        hand = BaseHand(*sample_cards)
        peeked = hand.peek(0, 1)
        self.assertEqual(len(hand), 3)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], sample_cards[0])

    def test_sort(self):
        cards = [self.card2, self.card1]
        hand = BaseHand(*cards)
        hand.sort()
        self.assertEqual(hand[0], cards[1])

    def test_is_empty(self):
        hand = BaseHand()
        self.assertTrue(hand.is_empty)

        hand.add_card(self.card1)
        self.assertFalse(hand.is_empty)
