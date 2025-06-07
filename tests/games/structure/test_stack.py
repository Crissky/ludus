import unittest
from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.stack import Stack
from typing import Generator


class TestStack(unittest.TestCase):
    def setUp(self):
        """Configura uma nova instância de Stack para ser usada antes
        de cada teste.
        """

        self.stack = Stack()
        self.card1 = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        self.card2 = Card(RoyalNames.KING, RoyalSuits.SPADES)
        self.card3 = Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)

    def test_init(self):
        """Teste inicialização da pilha.
        """

        self.assertIsInstance(self.stack, Stack)
        self.assertEqual(len(self.stack), 0)

    def test_push_single_card(self):
        """Teste push um único Card para a pilha.
        """

        self.stack.push(self.card1)
        self.assertEqual(len(self.stack), 1)
        self.assertEqual(self.stack[0], self.card1)

    def test_push_multiple_cards(self):
        """Teste push múltiplos Cards para a pilha.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        self.assertEqual(len(self.stack), 3)
        self.assertEqual(self.stack[0], self.card3)
        self.assertEqual(self.stack[1], self.card2)
        self.assertEqual(self.stack[2], self.card1)

    def test_push_no_cards(self):
        """Teste push nenhum Card para a pilha.
        """

        initial_length = len(self.stack)
        self.stack.push()
        self.assertEqual(len(self.stack), initial_length)

    def test_pop_single_item(self):
        """Teste de pop de um único item da pilha.
        """

        self.stack.push(self.card1, self.card2)
        popped = self.stack.pop()
        self.assertEqual(popped, self.card2)
        self.assertEqual(len(self.stack), 1)
        self.assertEqual(self.stack[0], self.card1)

    def test_pop_multiple_items(self):
        """Teste de pop de múltiplos itens da pilha.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        popped = self.stack.pop(2)
        self.assertIsInstance(popped, list)
        self.assertEqual(len(popped), 2)
        self.assertEqual(popped[0], self.card3)
        self.assertEqual(popped[1], self.card2)
        self.assertEqual(len(self.stack), 1)
        self.assertEqual(self.stack[0], self.card1)

    def test_pop_empty_stack(self):
        """Teste de pop de uma pilha vazia.
        """

        result = self.stack.pop()
        self.assertIsNone(result)

    def test_pop_zero_quantity(self):
        """Teste pop com quantity=0.
        """

        self.stack.push(self.card1)
        result = self.stack.pop(quantity=0)
        self.assertIsNone(result)
        self.assertEqual(len(self.stack.items), 1)

    def test_peek_empty_stack(self):
        """Teste peek uma pilha vazia.
        """

        result = self.stack.peek()
        self.assertIsNone(result)

    def test_peek_single_item(self):
        """Teste peek um único item da pilha.
        """

        self.stack.push(self.card1, self.card2)
        peeked = self.stack.peek()
        self.assertEqual(peeked, self.card2)
        self.assertEqual(self.stack[0], self.card2)
        self.assertEqual(self.stack[1], self.card1)
        self.assertEqual(len(self.stack.items), 2)

    def test_peek_multiple_items(self):
        """Teste peek múltiplos itens da pilha.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        peeked = self.stack.peek(2)
        self.assertIsInstance(peeked, list)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], self.card3)
        self.assertEqual(peeked[1], self.card2)
        self.assertEqual(self.stack[0], self.card3)
        self.assertEqual(self.stack[1], self.card2)
        self.assertEqual(self.stack[2], self.card1)
        self.assertEqual(len(self.stack.items), 3)

    def test_peek_more_than_available(self):
        """Test peek mais itens que os disponíveis na pilha.
        """

        self.stack.push(self.card1, self.card2)
        peeked = self.stack.peek(3)
        self.assertIsInstance(peeked, list)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], self.card2)
        self.assertEqual(peeked[1], self.card1)
        self.assertEqual(self.stack[0], self.card2)
        self.assertEqual(self.stack[1], self.card1)

    def test_iter_yields_cards_in_reverse_order(self):
        """Teste se o método __iter__ produz cartas na ordem inversa.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        cards_in_reverse = list(self.stack)
        self.assertEqual(len(cards_in_reverse), 3)
        self.assertEqual(cards_in_reverse[0], self.card3)
        self.assertEqual(cards_in_reverse[1], self.card2)
        self.assertEqual(cards_in_reverse[2], self.card1)

    def test_text_horizontal(self):
        """Teste se a propriedade text_horizontal retorna uma sequência de
        textos de cartas unidos por espaços.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        result = self.stack.text_horizontal
        expected_output = (
            f"{self.card3.suit.value}{self.card3.name.value} "
            f"{self.card2.suit.value}{self.card2.name.value} "
            f"{self.card1.suit.value}{self.card1.name.value}"
        )
        self.assertEqual(result, expected_output)

    def test_text_vertical(self):
        """Teste se a propriedade text_vertical une corretamente os
        textos dos cartões com quebras de linha.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        expected_output = (
            f"{self.card3.suit.value}{self.card3.name.value}\n"
            f"{self.card2.suit.value}{self.card2.name.value}\n"
            f"{self.card1.suit.value}{self.card1.name.value}"
        )
        self.assertEqual(self.stack.text_vertical, expected_output)

    def test_text_lazy(self):
        """Teste se a propriedade text_lazy retorna um gerador de valores de
        texto de cartas.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        expected = [
            self.card3.text,
            self.card2.text,
            self.card1.text,
        ]
        text_lazy_gen = self.stack.text_lazy
        self.assertIsInstance(text_lazy_gen, Generator)
        text_list = list(text_lazy_gen)
        self.assertEqual(text_list, expected)
