from bot.functions.enumeration import get_enum_index
from bot.games.cards.card import Card
from bot.games.enums.card import (
    ColorNames,
    ColorSuits,
    FlipColorNames,
    FlipColorSuits,
    FullRoyalNames,
    FullRoyalSuits,
    RoyalNames,
    RoyalSuits,
    SpanishNames,
    SpanishSuits,
    StrippedSpanishNames
)
import pytest
import unittest


class TestCard(unittest.TestCase):

    def setUp(self):
        # Cards 1
        self.ace_card1 = Card(RoyalNames.ACE, RoyalSuits.CLUBS)
        self.king_card1 = Card(RoyalNames.KING, RoyalSuits.CLUBS)
        self.number_card1 = Card(RoyalNames.TWO, RoyalSuits.CLUBS)

        self.full_king_card1 = Card(FullRoyalNames.KING, FullRoyalSuits.CLUBS)
        self.full_number_card1 = Card(FullRoyalNames.SIX, FullRoyalSuits.CLUBS)

        self.joker_card = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)

        self.block_card1 = Card(ColorNames.BLOCK, ColorSuits.RED)
        self.color_number_card1 = Card(ColorNames.ZERO, ColorSuits.RED)
        self.color_wild_card = Card(ColorNames.PLUS_ZERO, ColorSuits.BLACK)

        # Cards 2
        self.ace_card2 = Card(RoyalNames.ACE, RoyalSuits.DIAMONDS)
        self.king_card2 = Card(RoyalNames.KING, RoyalSuits.DIAMONDS)
        self.number_card2 = Card(RoyalNames.TWO, RoyalSuits.DIAMONDS)

        self.full_king_card2 = Card(
            FullRoyalNames.KING, FullRoyalSuits.DIAMONDS)
        self.full_number_card2 = Card(
            FullRoyalNames.SIX, FullRoyalSuits.DIAMONDS)

        # General Cards
        self.royal_number_card = Card(RoyalNames.TWO, RoyalSuits.CLUBS)
        self.full_royal_number_card = Card(
            FullRoyalNames.TWO, FullRoyalSuits.CLUBS)
        self.color_number_card = Card(ColorNames.ZERO, ColorSuits.RED)
        self.flip_color_number_card = Card(
            FlipColorNames.ZERO, FlipColorSuits.ORAGE)
        self.spanish_number_card = Card(SpanishNames.ONE, SpanishSuits.CLUBS)
        self.stripped_spanish_number_card = Card(
            StrippedSpanishNames.ONE, SpanishSuits.CLUBS)

    def test_init_invalid_name(self):
        """
        Teste para verificar se a inicialização de um Card com um tipo
        name inválido gera um TypeError.

        Este teste abrange o caso em que o parâmetro 'name' não é uma
        instância da enumeração Names,
        mas 'suit' é uma enumeração Suits válida. Ele verifica se um
        TypeError é gerado com a mensagem de erro apropriada.
        """

        invalid_name = "ACE"
        valid_suit = RoyalSuits.HEARTS
        error_text = 'name precisa ser um Enum do tipo Names.'

        with pytest.raises(TypeError, match=error_text):
            Card(invalid_name, valid_suit)

    def test_init_invalid_suit_type(self):
        """
        Teste se o método _init_ gera um TypeError quando um tipo
        inválido é fornecido para o parâmetro suit.
        """

        valid_name = RoyalNames.ACE
        invalid_suit = "HEARTS"
        error_text = 'suit precisa ser um Enum do tipo Suits.'
        with pytest.raises(TypeError, match=error_text):
            Card(valid_name, invalid_suit)

    def test_init_invalid_types(self):
        """
        Teste se o método _init_ gera um TypeError quando tipos inválidos
        são fornecidos.
        """

        invalid_name = "ACE"
        invalid_suit = "Invalid"
        error_text = 'name precisa ser um Enum do tipo Names.'
        with pytest.raises(TypeError, match=error_text):
            Card(invalid_name, invalid_suit)

    def test_eq_same_card(self):
        """
        Teste a igualdade de duas cartas idênticas.

        Este teste verifica se o método _eq_ identifica corretamente duas
        cartas como iguais quando têm o mesmo nome e naipe.
        """

        card1 = self.ace_card1
        card2 = self.ace_card1
        self.assertEqual(card1, card2)

    def test_eq_different_cards(self):
        """
        Teste a desigualdade de duas cartas diferentes.

        Este teste verifica se o método _eq_ identifica corretamente duas
        cartas como diferentes quando têm nomes ou naipes diferentes.
        """

        card1 = self.ace_card1
        card2 = self.king_card1
        self.assertNotEqual(card1, card2)

    def test_eq_non_card_object(self):
        """
        Teste o método _eq_ da classe Card ao comparar com um objeto que
        não seja Card.

        Este teste verifica se o método _eq_ retorna False quando o
        objeto 'other' não é uma instância da classe Card.
        """

        card = self.ace_card1
        non_card_object = card.text
        self.assertNotEqual(card, non_card_object)

    def test_eq_wilded_cards(self):
        """
        Teste a desigualdade de duas cartas diferentes que depois serão
        iguais após o valor do curinga ser escolhido.

        Este teste verifica se o método _eq_ identifica corretamente duas
        cartas como diferentes quando têm nomes ou naipes diferentes.
        """

        card1 = self.joker_card
        card2 = self.full_king_card1
        card2_name = card2.name
        card2_suit = card2.suit
        self.assertNotEqual(card1, card2)
        card1.set_wild(card2_name, card2_suit)
        self.assertEqual(card1, card2)

    def test_gt_same_card(self):
        """
        Teste se um card é maior que o outro.

        Este teste verifica se o método _gt_ identifica corretamente duas
        cartas como iguais quando têm o mesmo nome e naipe.
        """

        card1 = self.number_card1
        card2 = self.number_card1
        card3 = self.ace_card1
        self.assertFalse(card1 > card2)
        self.assertGreater(card1, card3)
        self.assertLess(card3, card1)

    def test_gt_non_card_object(self):
        """
        Teste o método _gt_ da classe Card ao comparar com um objeto que
        não seja Card.

        Este teste verifica se o método _gt_ retorna uma exceção quando o
        objeto 'other' não é uma instância da classe Card.
        """

        card = self.ace_card1
        non_card_object = 'ACE CLUBS'

        msg_error = (
            f'Espera um Card, obteve '
            f'{type(non_card_object)}({non_card_object})'
        )
        with self.assertRaises(TypeError) as context:
            card > non_card_object

        self.assertEqual(msg_error, str(context.exception))

    def test_hash(self):
        """
        Teste se o método _hash_ retorna o valor de hash
        esperado para uma instância de Card.
        """

        card = self.ace_card1
        expected_hash = hash((card.name, card.suit))
        self.assertEqual(hash(card), expected_hash)

    def test_repr(self):
        """
        Teste o método _repr_ retorna o valor correto.
        """

        card = self.ace_card1
        expected_repr = (
            f"Card({card.suit.value}{card.name.value})"
        )
        self.assertEqual(repr(card), expected_repr)

    def test_str_returns_text(self):
        """
        Teste se o método _str_ retorna a representação de texto do Card.
        """

        card = self.ace_card1
        expected_text = f"{card.suit.value}{card.name.value}"
        self.assertEqual(str(card), expected_text)

    def test_equals_name_card_type(self):
        """
        Teste se equals_name retorna True ao comparar com um objeto Card.
        """

        card = self.ace_card1
        other_card = self.ace_card1
        result = card.equals_name(other_card)
        msg = "equals_name deve retornar True para objetos Card com name igual"
        self.assertTrue(result, msg)

    def test_equals_name_names_type(self):
        """
        Teste se equals_name retorna True ao comparar com um objeto Names.
        """

        card = self.ace_card1
        other_name = card.name
        result = card.equals_name(other_name)
        msg = "equals_name deve retornar True para objetos Names igual"
        self.assertTrue(result, msg)

    def test_equals_name_card_type_different(self):
        """
        Teste se equals_name retorna False ao comparar com um objeto Card.
        """

        card = self.ace_card1
        other_card = self.king_card1
        result = card.equals_name(other_card)
        msg = (
            "equals_name deve retornar False para objetos Card com name "
            "diferente."
        )
        self.assertFalse(result, msg)

    def test_equals_name_names_type_different(self):
        """
        Teste se equals_name retorna False ao comparar com um objeto Names.
        """

        card = self.ace_card1
        other_name = self.king_card1.name
        result = card.equals_name(other_name)
        msg = "equals_name deve retornar False para objetos Names diferente."
        self.assertFalse(result, msg)

    def test_equals_name_different_type(self):
        """
        Teste se equals_name retorna False ao comparar com um objeto não-Card
        e não-Names.
        """

        card = self.ace_card1
        other = "Not a Card object"
        result = card.equals_name(other)
        msg = "equals_name deve retornar False para objetos que não Card/Names"
        self.assertFalse(result, msg)

    def test_equals_name_wilded(self):
        """
        Teste se equals_name retorna True ao comparar com um objeto Card
        e Names depois de setar o valor do curinga.
        """

        card = self.joker_card
        other_card = self.full_number_card1
        card.set_wild(other_card.name, other_card.suit)
        other_name = other_card.name
        result_card = card.equals_name(other_card)
        result_name = card.equals_name(other_name)
        msg = (
            "equals_name deve retornar True para objetos que não "
            "Card/Names idênticos"
        )
        self.assertTrue(result_card, msg)
        self.assertTrue(result_name, msg)

    def test_equals_suit_card_type(self):
        """
        Teste se equals_suit retorna True ao comparar com um objeto Card.
        """

        card = self.ace_card1
        other_card = self.ace_card1
        result = card.equals_suit(other_card)
        msg = "equals_suit deve retornar True para objetos Card com suit igual"
        self.assertTrue(result, msg)

    def test_equals_suit_suits_type(self):
        """
        Teste se equals_suit retorna True ao comparar com um objeto Suits.
        """

        card = self.ace_card1
        other_suit = card.suit
        result = card.equals_suit(other_suit)
        msg = "equals_suit deve retornar True para objetos Suits igual"
        self.assertTrue(result, msg)

    def test_equals_suit_card_type_different(self):
        """
        Teste se equals_suit retorna False ao comparar com um objeto Card.
        """

        card = self.ace_card1
        other_card = self.ace_card2
        result = card.equals_suit(other_card)
        msg = (
            "equals_suit deve retornar False para objetos Card com suit "
            "diferente"
        )
        self.assertFalse(result, msg)

    def test_equals_suit_suits_type_different(self):
        """
        Teste se equals_suit retorna False ao comparar com um objeto Suits.
        """

        card = self.ace_card1
        other_suit = self.ace_card2.suit
        result = card.equals_suit(other_suit)
        msg = "equals_suit deve retornar False para objetos Suits diferente."
        self.assertFalse(result, msg)

    def test_equals_suit_different_type(self):
        """
        Teste se equals_suit retorna False ao comparar com um objeto não-Card
        e não-Suits.
        """

        card = self.ace_card1
        other = "Not a Card object"
        result = card.equals_suit(other)
        msg = "equals_suit deve retornar False para objetos que não Card/Suits"
        self.assertFalse(result, msg)

    def test_equals_suit_wilded(self):
        """
        Teste se equals_suit retorna True ao comparar com um objeto Card
        e Suits depois de setar o valor do curinga.
        """

        card = self.joker_card
        other_card = self.full_number_card1
        card.set_wild(other_card.name, other_card.suit)
        other_name = other_card.suit
        result_card = card.equals_suit(other_card)
        result_name = card.equals_suit(other_name)
        msg = (
            "equals_suit deve retornar True para objetos que não "
            "Card/Suits idênticos"
        )
        self.assertTrue(result_card, msg)
        self.assertTrue(result_name, msg)

    def test_set_wild(self):
        """
        Teste se o método set_wild altera corretamente o valor do curinga.

        Esse teste também serve para testar as propriedades name e suit
        """

        card = self.joker_card
        new_name = self.full_number_card1.name
        new_suit = self.full_number_card1.suit
        self.assertEqual(card.name, FullRoyalNames.JOKER)
        self.assertEqual(card.suit, FullRoyalSuits.JOKER)
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)

        card.set_wild(new_name, new_suit)
        self.assertEqual(card.name, new_name)
        self.assertEqual(card.suit, new_suit)
        self.assertEqual(card.real_name, FullRoyalNames.JOKER)
        self.assertEqual(card.real_suit, FullRoyalSuits.JOKER)
        self.assertEqual(card.wild_name, new_name)
        self.assertEqual(card.wild_suit, new_suit)

    def test_set_wild_name(self):
        """
        Teste se o método set_wild_name altera corretamente o name do curinga.

        Esse teste também serve para testar as propriedades name
        """

        card = self.joker_card
        new_name = self.full_number_card1.name
        self.assertEqual(card.name, FullRoyalNames.JOKER)
        self.assertIsNone(card.wild_name)

        card.set_wild_name(new_name)
        self.assertEqual(card.name, new_name)
        self.assertEqual(card.real_name, FullRoyalNames.JOKER)
        self.assertEqual(card.wild_name, new_name)

    def test_set_wild_name_card_is_not_wild(self):
        """
        Teste se o método set_wild_name retorna um erro ao tentar alterar
        um Card não WILD.
        """

        card = self.full_king_card1
        self.assertEqual(card.name, FullRoyalNames.KING)
        self.assertIsNone(card.wild_name)

        with pytest.raises(ValueError, match=''):
            card.set_wild_name(FullRoyalNames.ACE)

    def test_set_wild_suit(self):
        """
        Teste se o método set_wild_suit altera corretamente o suit do curinga.

        Esse teste também serve para testar as propriedades suit
        """

        card = self.joker_card
        new_suit = self.full_king_card1.suit
        self.assertEqual(card.suit, FullRoyalSuits.JOKER)
        self.assertIsNone(card.wild_suit)

        card.set_wild_suit(new_suit)
        self.assertEqual(card.suit, new_suit)
        self.assertEqual(card.real_suit, FullRoyalSuits.JOKER)
        self.assertEqual(card.wild_suit, new_suit)

    def test_set_wild_suit_card_is_not_wild(self):
        """
        Teste se o método set_wild_suit retorna um erro ao tentar alterar
        um Card não WILD.
        """

        card = self.full_king_card1
        self.assertEqual(card.suit, FullRoyalSuits.CLUBS)
        self.assertIsNone(card.wild_suit)

        with pytest.raises(ValueError, match=''):
            card.set_wild_suit(FullRoyalSuits.SPADES)

    def test_text_returns_correct_string_representation(self):
        """
        Teste se a propriedade text retorna a representação correta
        da string do Card.

        Este teste verifica se a propriedade text de uma instância do
        Card combina corretamente o valor do naipe e o valor do nome
        para produzir a representação de string esperada.
        """

        card = self.ace_card1
        expected_text = f'{card.suit.value}{card.name.value}'
        self.assertEqual(card.text, expected_text)

    def test_value_returns_correct_index(self):
        """
        Teste se a propriedade value retorna o índice correto
        para um determinado nome de carta.

        Este teste verifica se a propriedade value de uma instância de
        Card chama corretamente a função get_enum_index com o nome
        da carta e retorna o resultado.
        """

        card = self.ace_card1
        expected_value = get_enum_index(card.name)
        self.assertEqual(card.value, expected_value)

    def test_value_valid_input(self):
        """
        Teste se a propriedade value retorna o índice enum correto
        para um nome de Card válido.
        """

        card = self.ace_card1
        self.assertEqual(card.value, 0)

    def test_suit_value(self):
        """
        Teste se a propriedade suit_value retorna o índice de enumeração
        correto para o naipe da carta.

        Este teste verifica se a propriedade suit_value chama
        corretamente get_enum_index com o naipe da carta e retorna o
        resultado esperado.
        """

        card = self.ace_card2
        expected_value = get_enum_index(card.suit)
        self.assertEqual(card.suit_value, expected_value)
        self.assertEqual(card.suit_value, 1)

    def test_unset_wild(self):
        """
        Teste o método unset_wild para garantir que ele redefina
        corretamente os atributos wild_name e wild_suit para None.
        Este teste cria um curinga, define seus valores curinga,
        depois os desfaz e verifica o resultado.
        """

        card = self.joker_card
        new_name = self.full_number_card1.name
        new_suit = self.full_number_card1.suit
        card.set_wild(new_name, new_suit)
        self.assertEqual(card.wild_name, new_name)
        self.assertEqual(card.name, new_name)
        self.assertEqual(card.wild_suit, new_suit)
        self.assertEqual(card.suit, new_suit)

        card.unset_wild()
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertEqual(card.name, FullRoyalNames.JOKER)
        self.assertEqual(card.suit, FullRoyalSuits.JOKER)

    def test_unset_wild_on_non_wild_card(self):
        """
        Teste unset_wild() em uma carta não curinga.
        Este teste verifica se a chamada de unset_wild() em uma carta comum
        (não curinga) não altera suas propriedades.
        """

        card = self.ace_card1
        original_name = card.name
        original_suit = card.suit

        card.unset_wild()

        self.assertEqual(card.name, original_name)
        self.assertEqual(card.suit, original_suit)
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)

    def test_is_wild(self):
        """
        Teste se o método is_wild retorna True para um Card curinga.
        """

        card1 = self.joker_card
        card2 = self.ace_card1
        self.assertTrue(card1.is_wild)
        self.assertFalse(card2.is_wild)

    def test_royal_number_card_names(self):
        """
        Teste se o método number_card_names retorna uma lista
        contendo todos os Cards de números de RoyalNames.
        """

        card = self.royal_number_card
        number_card_names = card.number_card_names
        expected_number_card_names = [
            RoyalNames.TWO, RoyalNames.THREE, RoyalNames.FOUR,
            RoyalNames.FIVE, RoyalNames.SIX, RoyalNames.SEVEN,
            RoyalNames.EIGHT, RoyalNames.NINE, RoyalNames.TEN
        ]
        for card_name in number_card_names:
            self.assertIn(card_name, expected_number_card_names)

    def test_full_royal_number_card_names(self):
        """
        Teste se o método number_card_names retorna uma lista
        contendo todos os Cards de números de FullRoyalNames.
        """

        card = self.full_royal_number_card
        number_card_names = card.number_card_names
        expected_number_card_names = [
            FullRoyalNames.TWO, FullRoyalNames.THREE, FullRoyalNames.FOUR,
            FullRoyalNames.FIVE, FullRoyalNames.SIX, FullRoyalNames.SEVEN,
            FullRoyalNames.EIGHT, FullRoyalNames.NINE, FullRoyalNames.TEN
        ]
        for card_name in number_card_names:
            self.assertIn(card_name, expected_number_card_names)

    def test_spanish_number_card_names(self):
        """
        Teste se o método number_card_names retorna uma lista
        contendo todos os Cards de números de SpanishNames.
        """

        card = self.spanish_number_card
        number_card_names = card.number_card_names
        expected_number_card_names = [
            SpanishNames.ONE, SpanishNames.TWO, SpanishNames.THREE,
            SpanishNames.FOUR, SpanishNames.FIVE, SpanishNames.SIX,
            SpanishNames.SEVEN, SpanishNames.EIGHT, SpanishNames.NINE,
            SpanishNames.KNAVE, SpanishNames.KNIGHT, SpanishNames.KING
        ]
        for card_name in number_card_names:
            self.assertIn(card_name, expected_number_card_names)

    def test_stripped_spanish_number_card_names(self):
        """
        Teste se o método number_card_names retorna uma lista
        contendo todos os Cards de números de StrippedSpanishNames.
        """

        card = self.stripped_spanish_number_card
        number_card_names = card.number_card_names
        expected_number_card_names = [
            StrippedSpanishNames.ONE, StrippedSpanishNames.TWO,
            StrippedSpanishNames.THREE, StrippedSpanishNames.FOUR,
            StrippedSpanishNames.FIVE, StrippedSpanishNames.SIX,
            StrippedSpanishNames.SEVEN, StrippedSpanishNames.KNAVE,
            StrippedSpanishNames.KNIGHT, StrippedSpanishNames.KING
        ]
        for card_name in number_card_names:
            self.assertIn(card_name, expected_number_card_names)

    def test_color_number_card_names(self):
        """
        Teste se o método number_card_names retorna uma lista
        contendo todos os Cards de números de ColorNames.
        """

        card = self.color_number_card
        number_card_names = card.number_card_names
        expected_number_card_names = [
            ColorNames.ZERO, ColorNames.ONE, ColorNames.TWO,
            ColorNames.THREE, ColorNames.FOUR, ColorNames.FIVE,
            ColorNames.SIX, ColorNames.SEVEN, ColorNames.EIGHT,
            ColorNames.NINE
        ]
        for card_name in number_card_names:
            self.assertIn(card_name, expected_number_card_names)

    def test_flip_color_number_card_names(self):
        """
        Teste se o método number_card_names retorna uma lista
        contendo todos os Cards de números de FlipColorNames.
        """

        card = self.flip_color_number_card
        number_card_names = card.number_card_names
        expected_number_card_names = [
            FlipColorNames.ZERO, FlipColorNames.ONE, FlipColorNames.TWO,
            FlipColorNames.THREE, FlipColorNames.FOUR, FlipColorNames.FIVE,
            FlipColorNames.SIX, FlipColorNames.SEVEN, FlipColorNames.EIGHT,
            FlipColorNames.NINE
        ]
        for card_name in number_card_names:
            self.assertIn(card_name, expected_number_card_names)
