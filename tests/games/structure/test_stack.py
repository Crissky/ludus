import random
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
        self.card_list = [self.card1, self.card2, self.card3]

    # Tests to Super Class
    def test_init(self):
        """Teste inicialização da pilha.
        """

        self.assertIsInstance(self.stack, Stack)
        self.assertEqual(len(self.stack), 0)

    def test_init_with_multiple_cards(self):
        """
        Teste o método _init_ de Stack com vários objetos Card.

        Verifica se o atributo items foi inicializado corretamente com
        os cards fornecidos.
        """

        stack = Stack(self.card1, self.card2, self.card3)

        self.assertEqual(len(stack), 3)
        self.assertEqual(stack[0], self.card3)
        self.assertEqual(stack[1], self.card2)
        self.assertEqual(stack[2], self.card1)

    def test_iter_yields_cards_in_order(self):
        """Teste se o método _iter_ produz cartas na ordem correta.
        """

        stack = Stack(*self.card_list)
        reversed_card_list = list(reversed(self.card_list))

        for i, card in enumerate(stack):
            self.assertEqual(card, reversed_card_list[i])

    def test_get_item(self):
        """
        Teste o acesso a um item específico usando o operador de indexação.
        """

        stack = Stack(*self.card_list)

        self.assertEqual(stack[0], self.card_list[2])
        self.assertEqual(stack[1], self.card_list[1])
        self.assertEqual(stack[2], self.card_list[0])

    def test_len(self):
        """ Teste se o método _len_ retorna o número correto de itens na Stack.
        """

        stack = Stack(*self.card_list)

        self.assertEqual(len(self.stack), 0)
        self.assertEqual(len(stack), 3)

    def test_shuffle_randomizes_order(self):
        """
        Teste se o método shuffle randomiza a ordem dos itens na Stack.

        Observe que há uma pequena chance de este teste falhar mesmo que
        o método shuffle esteja funcionando corretamente, devido à natureza da
        aleatoriedade.
        """

        stack = Stack(*self.card_list)
        original_order = stack.items.copy()
        random.seed(42)
        stack.shuffle()

        self.assertNotEqual(
            original_order,
            stack.items,
            "The shuffle method did not change the order of items"
        )
        self.assertEqual(
            set(original_order),
            set(stack.items),
            "The shuffle method changed the content of items"
        )

    # Tests Abstract Methods
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

    def test_push_bottom_single_card(self):
        """Teste push um único Card para a fila.
        """

        self.stack.push(self.card1)
        self.stack.push_botton(self.card2)
        self.assertEqual(len(self.stack), 2)
        self.assertEqual(self.stack[1], self.card2)
        self.assertEqual(self.stack[0], self.card1)

    def test_push_bottom_multiple_cards(self):
        """Teste push múltiplos Cards para a fila.
        """

        self.stack.push_botton(self.card1)
        self.stack.push_botton(self.card2, self.card3)
        self.assertEqual(len(self.stack), 3)
        self.assertEqual(self.stack[2], self.card2)
        self.assertEqual(self.stack[1], self.card3)
        self.assertEqual(self.stack[0], self.card1)

    def test_push_bottom_no_cards(self):
        """Teste push nenhum Card para a fila.
        """

        initial_length = len(self.stack)
        self.stack.push_botton()
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

    # Tests Properties
    def test_is_empty(self):
        """Teste se o property is_empty retorna True quando a Stack está vazia.
        """

        self.assertTrue(self.stack.is_empty)
        self.stack.push(self.card1)
        self.assertFalse(self.stack.is_empty)

    def test_text_horizintal(self):
        """Teste se o property text_horizontal retorna uma string com os
        cards na horizontal.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        expected = ' '.join((
            self.card3.text,
            self.card2.text,
            self.card1.text,
        ))
        self.assertEqual(self.stack.text_horizontal, expected)

    def test_text_horizintal_empty(self):
        """Teste se o property text_horizontal retorna uma string vazia
        quando a Stack está vazia.
        """

        expected = ""
        self.assertTrue(self.stack.is_empty)
        self.assertEqual(self.stack.text_horizontal, expected)

    def test_text_vertical(self):
        """Teste se o property text_horizontal retorna uma string com os
        cards na vertical.
        """

        self.stack.push(self.card1, self.card2, self.card3)
        expected = '\n'.join((
            self.card3.text,
            self.card2.text,
            self.card1.text,
        ))
        self.assertEqual(self.stack.text_vertical, expected)

    def test_text_vertical_empty(self):
        """Teste se o property text_horizontal retorna uma string com os
        cards na vertical.
        """

        expected = ""
        self.assertTrue(self.stack.is_empty)
        self.assertEqual(self.stack.text_vertical, expected)

    def test_text_lazy(self):
        """
        Teste se a propriedade text_lazy retorna um gerador de valores de
        texto de cartas.

        Verifica se o gerador produz o texto correto para cada carta
        na estrutura.
        """

        expected = [card.text for card in reversed(self.card_list)]
        self.stack.push(*self.card_list)
        text_lazy_gen = self.stack.text_lazy
        self.assertIsInstance(text_lazy_gen, Generator)
        text_list = list(text_lazy_gen)
        self.assertEqual(text_list, expected)

    def test_text_lazy_empty_structure(self):
        """
        Teste a propriedade text_lazy quando a Stack
        estiver vazia.

        Isso testa o caso extremo de uma estrutura vazia, que é tratado
        implicitamente pela expressão geradora na implementação do método.
        """

        lazy_text = self.stack.text_lazy
        self.assertIsInstance(lazy_text, Generator)
        self.assertEqual(list(lazy_text), [])
