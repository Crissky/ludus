from bot.games.cards.card import Card
from bot.games.cards.flex import FlexCard
from bot.games.enums.card import ColorNames, ColorSuits
import pytest
import unittest


class TestFlexCard(unittest.TestCase):

    def setUp(self):
        self.card = FlexCard(
            ColorNames.SEVEN,
            ColorSuits.GREEN,
            ColorSuits.BLUE
        )
        self.card_color = FlexCard(
            ColorNames.SEVEN,
            ColorSuits.GREEN,
            ColorSuits.BLUE
        )
        self.card_action = FlexCard(
            ColorNames.REVERSE,
            ColorSuits.GREEN,
            ColorNames.BLOCK
        )
        self.card_flex_none = FlexCard(
            ColorNames.REVERSE,
            ColorSuits.GREEN,
        )

    def test_init_correct_initialization(self):
        """
        Teste se o FlexCard foi inicializado corretamente com os atributos
        nome, naipe e flex.
        """

        name = ColorNames.ZERO
        suit = ColorSuits.YELLOW
        flex = ColorSuits.GREEN

        flex_card = FlexCard(name, suit, flex)

        self.assertEqual(flex_card.name, name)
        self.assertEqual(flex_card.suit, suit)
        self.assertEqual(flex_card.flex, flex)

    def test_init_invalid_flex(self):
        """
        Teste se o construtor FlexCard lança uma exceção ValueError
        quando o flex é inválido.
        """

        with pytest.raises(TypeError):
            FlexCard(
                ColorNames.REVERSE,
                ColorSuits.GREEN,
                "invalid_flex"
            )

    def test_eq_1(self):
        """
        Teste se o método __eq__ retorna True ao comparar dois objetos
        FlexCard com os mesmos atributos.

        Este teste abrange o caminho onde outro objeto possui o atributo
        "flex" e ambos os objetos são iguais.
        """

        self.assertTrue(self.card, self.card_color)

    def test_eq_2(self):
        """
        Teste se __eq__ retorna False ao comparar com um objeto
        que não tem o atributo 'flex'.
        """

        other_object = object()
        self.assertNotEqual(self.card, other_object)

    def test_hash_returns_consistent_hash(self):
        """
        Teste se o método __hash__ retorna um valor de hash consistente
        para uma instância de FlexCard.

        Este teste verifica se:
        1. O valor de hash é um inteiro
        2. Chamar __hash__ várias vezes no mesmo objeto retorna o mesmo valor
        3. Dois objetos FlexCard com os mesmos atributos têm o
        mesmo valor de hash.
        """

        hash1 = self.card.__hash__()
        hash2 = self.card.__hash__()
        hash3 = self.card_color.__hash__()
        msg1 = "Hash should be an integer"
        mag2 = "Hash should be consistent for the same object"
        msg3 = "Hash should be the same for equal objects"

        self.assertIsInstance(hash1, int, msg1)
        self.assertEqual(hash1, hash2, mag2)
        self.assertEqual(hash1, hash3, msg3)

    def test_equals_name_1(self):
        """
        Teste se equals_name retorna True quando other é uma
        enumeração Names e corresponde ao nome do cartão ou ao atributo flex.
        """

        self.assertTrue(self.card_action.equals_name(ColorNames.REVERSE))
        self.assertTrue(self.card_action.equals_name(ColorNames.BLOCK))
        self.assertFalse(self.card_action.equals_name(ColorNames.PLUS_TWO))

    def test_equals_name_2(self):
        """
        Teste se equals_name retorna True ao comparar um FlexCard com um Card
        onde o nome ou o atributo flex corresponde ao nome do Card.
        """

        other_card1 = Card(ColorNames.SEVEN, ColorSuits.RED)
        other_card2 = Card(ColorNames.SIX, ColorSuits.YELLOW)

        self.assertTrue(self.card.equals_name(other_card1))
        self.assertFalse(self.card.equals_name(other_card2))

    def test_equals_name_invalid_type(self):
        """
        Teste o método equals_name com um tipo de entrada inválido.
        Isso testa o tratamento explícito de entradas que
        não sejam Names e Card.
        """

        invalid_input = ColorNames.SEVEN.name
        self.assertFalse(self.card.equals_name(invalid_input))

    def test_equals_suit_1(self):
        """
        Testa o método equals_suit ao comparar uma FlexCard com um Suit.
        Verifica se o método retorna True se o naipe da carta
        ou o atributo flex corresponder ao Suit fornecido,
        e False caso contrário.
        """

        self.assertTrue(self.card.equals_suit(ColorSuits.GREEN))
        self.assertTrue(self.card.equals_suit(ColorSuits.BLUE))
        self.assertFalse(self.card.equals_suit(ColorSuits.RED))

    def test_equals_suit_2(self):
        """
        Testa o método equals_suit quando o outro objeto é uma
        instância de Card.

        Verifica se o método compara corretamente o naipe da FlexCard
        com o naipe da outra Card, considerando tanto o naipe primário
        quanto o naipe flexível.
        """

        other_card1 = Card(ColorNames.ZERO, ColorSuits.GREEN)
        other_card2 = Card(ColorNames.ZERO, ColorSuits.BLUE)
        other_card3 = Card(ColorNames.ZERO, ColorSuits.YELLOW)

        self.assertTrue(self.card_color.equals_suit(other_card1))
        self.assertTrue(self.card_color.equals_suit(other_card2))
        self.assertFalse(self.card_color.equals_suit(other_card3))

    def test_equals_suit_invalid_type(self):
        """
        Teste o método equals_suit com um tipo de entrada inválido.
        Este teste verifica se o método retorna False quando recebe uma entrada
        que não seja um Card nem enumeração Suits.
        """

        invalid_input = ColorSuits.GREEN.name
        self.assertFalse(self.card_color.equals_suit(invalid_input))

    def test_text_1(self):
        """
        Teste se a propriedade text do FlexCard retorna a representação de
        string correta.

        Este teste verifica se a propriedade text combina o valor suit,
        o valor name e o valor flex no
        formato: '{suit_value}{name_value}({flex_value})'.
        """

        suit = self.card.suit
        name = self.card.name
        flex = self.card.flex
        expected_text = f"{suit.value}{name.value}({flex.value})"
        self.assertEqual(self.card.text, expected_text)

    def test_text_flex_is_none(self):
        """
        Teste se a propriedade text do FlexCard retorna a representação de
        string correta quando o atributo flex é None.

        Este teste verifica se a propriedade text combina o valor suit
        e o valor name no formato: '{suit_value}{name_value}'.
        """

        suit = self.card_flex_none.suit
        name = self.card_flex_none.name
        expected_text = f"{suit.value}{name.value}"
        self.assertEqual(self.card_flex_none.text, expected_text)
