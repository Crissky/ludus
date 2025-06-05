import unittest
from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.queue import Queue


class TestQueue(unittest.TestCase):
    def setUp(self):
        """Configura uma nova instância de Queue para ser usada antes
        de cada teste.
        """

        self.queue = Queue()
        self.card1 = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        self.card2 = Card(RoyalNames.KING, RoyalSuits.SPADES)
        self.card3 = Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)

    def test_push_single_card(self):
        """Teste push um único Card para a fila."""

        self.queue.push(self.card1)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.card1)

    def test_push_multiple_cards(self):
        """Teste push múltiplos Cards para a fila."""

        self.queue.push(self.card1, self.card2, self.card3)
        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
        self.assertEqual(self.queue[2], self.card3)

    def test_push_no_cards(self):
        """Teste push nenhum Card para a fila."""

        initial_length = len(self.queue)
        self.queue.push()
        self.assertEqual(len(self.queue), initial_length)

    def test_pop_single_item(self):
        """Teste de pop de um único item da queue."""

        self.queue.push(self.card1, self.card2)
        popped = self.queue.pop()
        self.assertEqual(popped, self.card1)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.card2)

    def test_pop_multiple_items(self):
        """Teste de pop de múltiplos itens da queue."""

        self.queue.push(self.card1, self.card2, self.card3)
        popped = self.queue.pop(2)
        self.assertIsInstance(popped, list)
        self.assertEqual(len(popped), 2)
        self.assertEqual(popped[0], self.card1)
        self.assertEqual(popped[1], self.card2)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.card3)

    def test_pop_empty_queue(self):
        """Teste de pop de uma queue vazia."""

        result = self.queue.pop()
        self.assertIsNone(result)

    def test_pop_zero_quantity(self):
        """Teste pop com quantity=0."""

        self.queue.push(self.card1)
        result = self.queue.pop(0)
        self.assertIsNone(result)
        self.assertEqual(len(self.queue.items), 1)

    def test_peek_empty_queue(self):
        """Teste peek uma queue vazia."""

        result = self.queue.peek()
        self.assertIsNone(result)

    def test_peek_single_item(self):
        """Test peek um único item da queue."""

        self.queue.push(self.card1, self.card2)
        peeked = self.queue.peek()
        self.assertEqual(peeked, self.card1)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
        self.assertEqual(len(self.queue.items), 2)

    def test_peek_multiple_items(self):
        """Test peek múltiplos itens da queue."""

        self.queue.push(self.card1, self.card2, self.card3)
        peeked = self.queue.peek(2)
        self.assertIsInstance(peeked, list)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], self.card1)
        self.assertEqual(peeked[1], self.card2)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
        self.assertEqual(self.queue[2], self.card3)
        self.assertEqual(len(self.queue.items), 3)

    def test_peek_more_than_available(self):
        """Test peek mais itens que os disponíveis na queue."""

        self.queue.push(self.card1, self.card2)
        peeked = self.queue.peek(3)
        self.assertIsInstance(peeked, list)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], self.card1)
        self.assertEqual(peeked[1], self.card2)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
