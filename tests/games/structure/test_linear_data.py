from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.linear_data import LinearDataStructure
from typing import Generator
import random
import unittest


class TestLinearData(unittest.TestCase):

    def test_init_with_multiple_cards(self):
        """
        Teste o método _init_ de LinearDataStructure com vários objetos Card.

        Verifica se o atributo items foi inicializado corretamente com
        os cards fornecidos.
        """

        card1 = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        card2 = Card(RoyalNames.KING, RoyalSuits.SPADES)
        card3 = Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)

        linear_data = LinearDataStructure(card1, card2, card3)

        self.assertEqual(len(linear_data), 3)
        self.assertEqual(linear_data[0], card1)
        self.assertEqual(linear_data[1], card2)
        self.assertEqual(linear_data[2], card3)

    def test_init_with_no_arguments(self):
        """
        Teste a inicialização de LinearDataStructure sem argumentos.
        Este é um caso extremo em que o parâmetro *args está vazio.
        """

        linear_data = LinearDataStructure()
        self.assertEqual(len(linear_data), 0)

    def test_iter_yields_cards_in_order(self):
        """
        Teste se o método _iter_ produz cartas na ordem correta.
        """

        card1 = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        card2 = Card(RoyalNames.KING, RoyalSuits.SPADES)
        card3 = Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)
        card_list = [card1, card2, card3]
        linear_data = LinearDataStructure(card1, card2, card3)

        for i, card in enumerate(linear_data):
            self.assertEqual(card, card_list[i])

    def test_get_item(self):
        """
        Teste o acesso a um item específico usando o operador de indexação.
        """

        cards = [
            Card(RoyalNames.ACE, RoyalSuits.HEARTS),
            Card(RoyalNames.KING, RoyalSuits.SPADES),
            Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS),
        ]
        linear_data = LinearDataStructure(*cards)

        self.assertEqual(linear_data[0], cards[0])
        self.assertEqual(linear_data[1], cards[1])
        self.assertEqual(linear_data[2], cards[2])

    def test_len(self):
        """
        Teste se o método _len_ retorna o número correto de itens na
        LinearDataStructure.
        """

        cards = [
            Card(RoyalNames.ACE, RoyalSuits.HEARTS),
            Card(RoyalNames.KING, RoyalSuits.SPADES),
            Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS),
        ]
        linear_data = LinearDataStructure(*cards)

        self.assertEqual(len(linear_data), 3)

    def test_len_empty_structure(self):
        """
        Teste se _len_ retorna 0 para uma LinearDataStructure vazia.
        Este é um caso extremo, pois testa o comportamento quando
        não há itens presentes.
        """

        linear_data = LinearDataStructure()
        self.assertEqual(len(linear_data), 0)

    def test_shuffle_randomizes_order(self):
        """
        Teste se o método shuffle randomiza a ordem dos itens na
        LinearDataStructure.

        Observe que há uma pequena chance de este teste falhar mesmo que
        o método shuffle esteja funcionando corretamente, devido à natureza da
        aleatoriedade.
        """

        cards = [
            Card(RoyalNames.ACE, RoyalSuits.SPADES),
            Card(RoyalNames.KING, RoyalSuits.HEARTS),
            Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS),
            Card(RoyalNames.JACK, RoyalSuits.CLUBS)
        ]
        linear_data = LinearDataStructure(*cards)
        original_order = linear_data.items.copy()
        random.seed(42)
        linear_data.shuffle()

        self.assertNotEqual(
            original_order,
            linear_data.items,
            "The shuffle method did not change the order of items"
        )

        self.assertEqual(
            set(original_order),
            set(linear_data.items),
            "The shuffle method changed the content of items"
        )

    def test_is_empty(self):
        """
        Teste para verificar se is_empty retorna True para uma
        LinearDataStructure vazia.

        Este teste verifica se o método is_empty identifica corretamente
        quando a LinearDataStructure não contém itens.
        """

        linear_data = LinearDataStructure()
        self.assertTrue(linear_data.is_empty)

    def test_is_empty_with_items(self):
        """
        Teste o método is_empty quando a LinearDataStructure tiver itens.

        Este não é um teste estritamente negativo, mas verifica a condição
        oposta para garantir que o método funcione corretamente para
        estruturas não vazias.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        linear_data = LinearDataStructure(card)
        self.assertFalse(linear_data.is_empty)

    def test_text_horizontal(self):
        """
        Teste se a propriedade text_horizontal retorna uma sequência de
        textos de cartas unidos por espaços.
        """

        cards = [
            Card(RoyalNames.ACE, RoyalSuits.HEARTS),
            Card(RoyalNames.KING, RoyalSuits.SPADES),
            Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)
        ]
        linear_data = LinearDataStructure(*cards)
        result = linear_data.text_horizontal
        expected = (
            f"{RoyalSuits.HEARTS.value}{RoyalNames.ACE.value} "
            f"{RoyalSuits.SPADES.value}{RoyalNames.KING.value} "
            f"{RoyalSuits.DIAMONDS.value}{RoyalNames.QUEEN.value}"
        )
        self.assertEqual(
            result,
            expected,
            f"Expected '{expected}', but got '{result}'"
        )

    def test_text_horizontal_empty_structure(self):
        """
        Teste a propriedade text_horizontal quando a LinearDataStructure
        estiver vazia.

        Isso testa o caso extremo de uma estrutura vazia, que é tratado
        implicitamente pela operação join na implementação do método.
        """

        empty_structure = LinearDataStructure()
        self.assertEqual(empty_structure.text_horizontal, "")

    def test_text_vertical(self):
        """
        Teste se a propriedade text_vertical une corretamente os
        textos dos cartões com quebras de linha.
        """

        cards = [
            Card(RoyalNames.ACE, RoyalSuits.HEARTS),
            Card(RoyalNames.KING, RoyalSuits.SPADES),
            Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)
        ]
        expected_output = (
            f"{RoyalSuits.HEARTS.value}{RoyalNames.ACE.value}\n"
            f"{RoyalSuits.SPADES.value}{RoyalNames.KING.value}\n"
            f"{RoyalSuits.DIAMONDS.value}{RoyalNames.QUEEN.value}"
        )
        linear_data = LinearDataStructure(*cards)
        self.assertEqual(linear_data.text_vertical, expected_output)

    def test_text_vertical_empty_structure(self):
        """
        Teste a propriedade text_vertical quando a LinearDataStructure
        estiver vazia.

        Isso testa o caso extremo de uma estrutura vazia, que é tratado
        implicitamente pela operação join na implementação do método.
        """

        linear_data = LinearDataStructure()
        self.assertEqual(linear_data.text_vertical, "")

    def test_text_lazy(self):
        """
        Teste se a propriedade text_lazy retorna um gerador de valores de
        texto de cartas.

        Verifica se o gerador produz o texto correto para cada carta
        na estrutura.
        """

        cards = [
            Card(RoyalNames.ACE, RoyalSuits.SPADES),
            Card(RoyalNames.KING, RoyalSuits.HEARTS),
            Card(RoyalNames.QUEEN, RoyalSuits.DIAMONDS)
        ]
        expected = [
            f"{RoyalSuits.SPADES.value}{RoyalNames.ACE.value}",
            f"{RoyalSuits.HEARTS.value}{RoyalNames.KING.value}",
            f"{RoyalSuits.DIAMONDS.value}{RoyalNames.QUEEN.value}",
        ]
        linear_data = LinearDataStructure(*cards)
        text_lazy_gen = linear_data.text_lazy
        self.assertIsInstance(text_lazy_gen, Generator)
        text_list = list(text_lazy_gen)
        self.assertEqual(text_list, expected)

    def test_text_lazy_empty_structure(self):
        """
        Teste a propriedade text_lazy quando a LinearDataStructure
        estiver vazia.

        Isso testa o caso extremo de uma estrutura vazia, que é tratado
        implicitamente pela expressão geradora na implementação do método.
        """

        empty_structure = LinearDataStructure()
        lazy_text = empty_structure.text_lazy
        self.assertIsInstance(lazy_text, Generator)
        self.assertEqual(list(lazy_text), [])
