import unittest
from unittest.mock import MagicMock

from bot.games.structure.linear_data import LinearDataStructure
from bot.games.cards.card import Card


class ConcreteLinearData(LinearDataStructure):
    def push(self, *cards: Card):
        self.items.extend(cards)

    def push_bottom(self, *cards: Card):
        for card in reversed(cards):
            self.items.insert(0, card)

    def pop(self, quantity: int = 1):
        if quantity == 1:
            return self.items.pop()
        return [self.items.pop() for _ in range(quantity)]

    def peek(self, quantity: int = 1):
        if quantity == 1:
            return self.items[-1]
        return self.items[-quantity:]

    def peek_bottom(self, quantity: int = 1):
        if quantity == 1:
            return self.items[0]
        return self.items[:quantity]


class TestLinearDataStructure(unittest.TestCase):
    def setUp(self):
        self.mock_card1 = MagicMock(spec=Card)
        self.mock_card1.text = 'Card 1'

        self.mock_card2 = MagicMock(spec=Card)
        self.mock_card2.text = 'Card 2'

    def test_init_empty(self):
        data = ConcreteLinearData()

        self.assertEqual(len(data), 0)
        self.assertTrue(data.is_empty)

    def test_init_with_card(self):
        data = ConcreteLinearData(self.mock_card1)

        self.assertEqual(len(data), 1)
        self.assertFalse(data.is_empty)

    def test_init_with_cards(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        self.assertEqual(len(data), 2)
        self.assertFalse(data.is_empty)

    def test_bool_empty(self):
        data = ConcreteLinearData()

        self.assertFalse(bool(data))

    def test_bool_with_card(self):
        data = ConcreteLinearData(self.mock_card1)

        self.assertTrue(bool(data))

    def test_bool_with_cards(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        self.assertTrue(bool(data))

    def test_iter(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        cards = list(data)

        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0], self.mock_card1)
        self.assertEqual(cards[1], self.mock_card2)

    def test_getitem(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        self.assertEqual(data[0], self.mock_card1)
        self.assertEqual(data[1], self.mock_card2)

    def test_len(self):
        data = ConcreteLinearData()
        self.assertEqual(len(data), 0)

        data.push(self.mock_card1)
        self.assertEqual(len(data), 1)

    def test_shuffle(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)
        original_items = data.items.copy()

        data.shuffle()

        self.assertEqual(len(data.items), len(original_items))

    def test_is_empty_property(self):
        data = ConcreteLinearData()
        self.assertTrue(data.is_empty)

        data.push(self.mock_card1)
        self.assertFalse(data.is_empty)

    def test_text_horizontal(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        result = data.text_horizontal

        self.assertEqual(result, 'Card 1 Card 2')

    def test_text_vertical(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        result = data.text_vertical

        self.assertEqual(result, 'Card 1\nCard 2')

    def test_text_lazy(self):
        data = ConcreteLinearData(self.mock_card1, self.mock_card2)

        result = list(data.text_lazy)

        self.assertEqual(result, ['Card 1', 'Card 2'])
