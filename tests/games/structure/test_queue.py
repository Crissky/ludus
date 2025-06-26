import random
from typing import Generator
import unittest

from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.queue import Queue


class TestQueue(unittest.TestCase):
    def setUp(self):
        """
        Configura uma nova instância de Queue para ser usada antes
        de cada teste.
        """

        self.queue = Queue()
        self.card1 = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        self.card2 = Card(RoyalNames.KING, RoyalSuits.SPADES)
        self.card3 = Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)
        self.card_list = [self.card1, self.card2, self.card3]

    # Tests to Super Class
    def test_init_with_multiple_cards(self):
        """
        Teste o método _init_ de Queue com vários objetos Card.

        Verifica se o atributo items foi inicializado corretamente com
        os cards fornecidos.
        """

        queue = Queue(self.card1, self.card2, self.card3)

        self.assertEqual(len(queue), 3)
        self.assertEqual(queue[0], self.card1)
        self.assertEqual(queue[1], self.card2)
        self.assertEqual(queue[2], self.card3)

    def test_bool(self):
        """
        Teste o método __bool__ com a queue vazio que com um e mais Cards
        """

        self.assertFalse(self.queue)
        self.queue.push(self.card1)
        self.assertTrue(self.queue)
        self.queue.push(self.card2)
        self.assertTrue(self.queue)

    def test_iter_yields_cards_in_order(self):
        """Teste se o método _iter_ produz cartas na ordem correta.
        """

        queue = Queue(*self.card_list)

        for i, card in enumerate(queue):
            self.assertEqual(card, self.card_list[i])

    def test_get_item(self):
        """
        Teste o acesso a um item específico usando o operador de indexação.
        """

        queue = Queue(*self.card_list)

        self.assertEqual(queue[0], self.card_list[0])
        self.assertEqual(queue[1], self.card_list[1])
        self.assertEqual(queue[2], self.card_list[2])

    def test_len(self):
        """ Teste se o método _len_ retorna o número correto de itens na Queue.
        """

        queue = Queue(*self.card_list)

        self.assertEqual(len(self.queue), 0)
        self.assertEqual(len(queue), 3)

    def test_shuffle_randomizes_order(self):
        """
        Teste se o método shuffle randomiza a ordem dos itens na Queue.

        Observe que há uma pequena chance de este teste falhar mesmo que
        o método shuffle esteja funcionando corretamente, devido à natureza da
        aleatoriedade.
        """

        queue = Queue(*self.card_list)
        original_order = queue.items.copy()
        random.seed(42)
        queue.shuffle()

        self.assertNotEqual(
            original_order,
            queue.items,
            "The shuffle method did not change the order of items"
        )
        self.assertEqual(
            set(original_order),
            set(queue.items),
            "The shuffle method changed the content of items"
        )

    # Tests Abstract Methods
    def test_push_single_card(self):
        """Teste push um único Card para a queue.
        """

        self.queue.push(self.card1)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.card1)

    def test_push_multiple_cards(self):
        """Teste push múltiplos Cards para a queue.
        """

        self.queue.push(self.card1)
        self.queue.push(self.card2, self.card3)
        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
        self.assertEqual(self.queue[2], self.card3)

    def test_push_no_cards(self):
        """Teste push nenhum Card para a queue.
        """

        initial_length = len(self.queue)
        self.queue.push()
        self.assertEqual(len(self.queue), initial_length)

    def test_push_not_card_type(self):
        """Teste push um objeto que não é um Card para a queue.
        """

        not_card = "not a card"
        msg_error = f"Espera um Card, obteve {type(not_card)}({not_card})"
        with self.assertRaises(TypeError) as context:
            self.queue.push(not_card)

        self.assertEqual(str(context.exception), msg_error)

    def test_push_bottom_single_card(self):
        """Teste push um único Card para a queue.
        """

        self.queue.push(self.card1)
        self.queue.push_bottom(self.card2)
        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue[0], self.card2)
        self.assertEqual(self.queue[1], self.card1)

    def test_push_bottom_multiple_cards(self):
        """Teste push múltiplos Cards para a queue.
        """

        self.queue.push_bottom(self.card1)
        self.queue.push_bottom(self.card2, self.card3)
        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue[0], self.card2)
        self.assertEqual(self.queue[1], self.card3)
        self.assertEqual(self.queue[2], self.card1)

    def test_push_bottom_no_cards(self):
        """Teste push nenhum Card para a queue.
        """

        initial_length = len(self.queue)
        self.queue.push_bottom()
        self.assertEqual(len(self.queue), initial_length)

    def test_push_bottom_not_card_type(self):
        """Teste push_bottom um objeto que não é um Card para a queue.
        """

        not_card = "not a card"
        msg_error = f"Espera um Card, obteve {type(not_card)}({not_card})"
        with self.assertRaises(TypeError) as context:
            self.queue.push_bottom(not_card)

        self.assertEqual(str(context.exception), msg_error)

    def test_pop_single_item(self):
        """Teste de pop de um único item da queue.
        """

        self.queue.push(self.card1, self.card2)
        popped = self.queue.pop()
        self.assertEqual(popped, self.card1)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.card2)

    def test_pop_multiple_items(self):
        """Teste de pop de múltiplos itens da queue.
        """

        self.queue.push(self.card1, self.card2, self.card3)
        popped = self.queue.pop(2)
        self.assertIsInstance(popped, list)
        self.assertEqual(len(popped), 2)
        self.assertEqual(popped[0], self.card1)
        self.assertEqual(popped[1], self.card2)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.card3)

    def test_pop_empty_queue(self):
        """Teste de pop de uma queue vazia.
        """

        result = self.queue.pop()
        self.assertIsNone(result)

    def test_pop_zero_quantity(self):
        """Teste pop com quantity=0.
        """

        self.queue.push(self.card1)
        result = self.queue.pop(0)
        self.assertIsNone(result)
        self.assertEqual(len(self.queue.items), 1)

    def test_peek_empty_queue(self):
        """Teste peek uma queue vazia.
        """

        result = self.queue.peek()
        self.assertIsNone(result)

    def test_peek_single_item(self):
        """Test peek um único item da queue.
        """

        self.queue.push(self.card1, self.card2)
        peeked = self.queue.peek()
        self.assertEqual(peeked, self.card1)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
        self.assertEqual(len(self.queue.items), 2)

    def test_peek_multiple_items(self):
        """Test peek múltiplos itens da queue.
        """

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
        """Test peek mais itens que os disponíveis na queue.
        """

        self.queue.push(self.card1, self.card2)
        peeked = self.queue.peek(3)
        self.assertIsInstance(peeked, list)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], self.card1)
        self.assertEqual(peeked[1], self.card2)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)

    # Tests Properties
    def test_is_empty(self):
        """Teste se o property is_empty retorna True quando a Queue está vazia.
        """

        self.assertTrue(self.queue.is_empty)
        self.queue.push(self.card1)
        self.assertFalse(self.queue.is_empty)

    def test_text_horizintal(self):
        """Teste se o property text_horizontal retorna uma string com os
        cards na horizontal.
        """

        self.queue.push(self.card1, self.card2, self.card3)
        expected = ' '.join((
            self.card1.text,
            self.card2.text,
            self.card3.text,
        ))
        self.assertEqual(self.queue.text_horizontal, expected)

    def test_text_horizintal_empty(self):
        """Teste se o property text_horizontal retorna uma string vazia
        quando a Queue está vazia.
        """

        expected = ""
        self.assertTrue(self.queue.is_empty)
        self.assertEqual(self.queue.text_horizontal, expected)

    def test_text_vertical(self):
        """Teste se o property text_horizontal retorna uma string com os
        cards na vertical.
        """

        self.queue.push(self.card1, self.card2, self.card3)
        expected = '\n'.join((
            self.card1.text,
            self.card2.text,
            self.card3.text,
        ))
        self.assertEqual(self.queue.text_vertical, expected)

    def test_text_vertical_empty(self):
        """Teste se o property text_horizontal retorna uma string com os
        cards na vertical.
        """

        expected = ""
        self.assertTrue(self.queue.is_empty)
        self.assertEqual(self.queue.text_vertical, expected)

    def test_text_lazy(self):
        """
        Teste se a propriedade text_lazy retorna um gerador de valores de
        texto de cartas.

        Verifica se o gerador produz o texto correto para cada carta
        na estrutura.
        """

        expected = [card.text for card in self.card_list]
        self.queue.push(*self.card_list)
        text_lazy_gen = self.queue.text_lazy
        self.assertIsInstance(text_lazy_gen, Generator)
        text_list = list(text_lazy_gen)
        self.assertEqual(text_list, expected)

    def test_text_lazy_empty_structure(self):
        """
        Teste a propriedade text_lazy quando a Queue
        estiver vazia.

        Isso testa o caso extremo de uma estrutura vazia, que é tratado
        implicitamente pela expressão geradora na implementação do método.
        """

        lazy_text = self.queue.text_lazy
        self.assertIsInstance(lazy_text, Generator)
        self.assertEqual(list(lazy_text), [])

    def test_peek_bottom_single_item(self):
        """
        Teste o método peek_bottom quando a quantidade for 1 e a queue
        não estiver vazia.

        Este teste verifica se peek_bottom retorna o último item da queue
        sem removê-lo quando a quantidade for 1 e a queue não estiver vazia.
        """
        self.queue.push(self.card1, self.card2, self.card3)
        peeked = self.queue.peek_bottom()
        self.assertEqual(peeked, self.card3)
        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue[-1], self.card3)

    def test_peek_bottom_empty_queue(self):
        """
        Teste peek_bottom em uma queue vazia com quantidade=1 e quantidade>1.

        Este teste abrange o caso em que a queue está vazia,
        o que deve retornar None, independentemente do parâmetro quantidade.
        """

        peeked1 = self.queue.peek_bottom()
        peeked2 = self.queue.peek_bottom(2)
        self.assertIsNone(peeked1)
        self.assertIsNone(peeked2)

    def test_peek_bottom_multiple_items(self):
        """
        Teste o método peek_bottom com vários itens na queue.

        Este teste verifica se peek_bottom retorna o número correto de itens
        do final da queue sem modificar o conteúdo da queue.
        """

        self.queue.push(self.card1, self.card2, self.card3)
        peeked = self.queue.peek_bottom(2)

        self.assertIsInstance(peeked, list)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(peeked[0], self.card2)
        self.assertEqual(peeked[1], self.card3)
        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue[0], self.card1)
        self.assertEqual(self.queue[1], self.card2)
        self.assertEqual(self.queue[2], self.card3)

    def test_peek_bottom_quantity_zero(self):
        """
        Teste peek_bottom com quantity=0 para garantir que retorne None.
        Isso testa o caso extremo em que uma quantidade inválida é fornecida.
        """

        self.queue.push(self.card1)
        result = self.queue.peek_bottom(0)
        self.assertIsNone(result)
