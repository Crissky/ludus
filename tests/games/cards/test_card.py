from bot.functions.enumeration import get_enum_index
from bot.games.cards.card import Card
from bot.games.enums.card import (
    FullRoyalNames,
    FullRoyalSuits,
    RoyalNames,
    RoyalSuits
)
import pytest
import unittest


class TestCard(unittest.TestCase):

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

        card1 = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        card2 = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        self.assertEqual(card1, card2)

    def test_eq_different_cards(self):
        """
        Teste a desigualdade de duas cartas diferentes.

        Este teste verifica se o método _eq_ identifica corretamente duas
        cartas como diferentes quando têm nomes ou naipes diferentes.
        """

        card1 = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        card2 = Card(RoyalNames.KING, RoyalSuits.HEARTS)
        self.assertNotEqual(card1, card2)

    def test_eq_non_card_object(self):
        """
        Teste o método _eq_ da classe Card ao comparar com um objeto que
        não seja Card.

        Este teste verifica se o método _eq_ retorna False quando o
        objeto 'outro' não é uma instância da classe Card.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        non_card_object = card.text
        self.assertNotEqual(card, non_card_object)

    def test_eq_wilded_cards(self):
        """
        Teste a desigualdade de duas cartas diferentes que depois serão
        iguais após o valor do curinga ser escolhido.

        Este teste verifica se o método _eq_ identifica corretamente duas
        cartas como diferentes quando têm nomes ou naipes diferentes.
        """

        card1 = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)
        card2 = Card(FullRoyalNames.KING, FullRoyalSuits.HEARTS)
        self.assertNotEqual(card1, card2)
        card1.set_wild(FullRoyalNames.KING, FullRoyalSuits.HEARTS)
        self.assertEqual(card1, card2)

    def test_hash(self):
        """
        Teste se o método _hash_ retorna o valor de hash
        esperado para uma instância de Card.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        expected_hash = hash((RoyalNames.ACE, RoyalSuits.SPADES))
        self.assertEqual(hash(card), expected_hash)

    def test_repr(self):
        """
        Teste o método _repr_ retorna o valor correto.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        expected_repr = (
            f"Card({RoyalSuits.SPADES.value}{RoyalNames.ACE.value})"
        )
        self.assertEqual(repr(card), expected_repr)

    def test_str_returns_text(self):
        """
        Teste se o método _str_ retorna a representação de texto do Card.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        expected_text = f"{RoyalSuits.SPADES.value}{RoyalNames.ACE.value}"
        self.assertEqual(str(card), expected_text)

    def test_equals_name_card_type(self):
        """
        Teste se equals_name retorna True ao comparar com um objeto Card.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        result = card.equals_name(other_card)
        msg = "equals_name deve retornar True para objetos Card com name igual"
        self.assertTrue(result, msg)

    def test_equals_name_names_type(self):
        """
        Teste se equals_name retorna True ao comparar com um objeto Names.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_name = RoyalNames.ACE
        result = card.equals_name(other_name)
        msg = "equals_name deve retornar True para objetos Names igual"
        self.assertTrue(result, msg)

    def test_equals_name_card_type_different(self):
        """
        Teste se equals_name retorna False ao comparar com um objeto Card.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_card = Card(RoyalNames.KING, RoyalSuits.SPADES)
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

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_name = RoyalNames.KING
        result = card.equals_name(other_name)
        msg = "equals_name deve retornar False para objetos Names diferente."
        self.assertFalse(result, msg)

    def test_equals_name_different_type(self):
        """
        Teste se equals_name retorna False ao comparar com um objeto não-Card
        e não-Names.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other = "Not a Card object"
        result = card.equals_name(other)
        msg = "equals_name deve retornar False para objetos que não Card/Names"
        self.assertFalse(result, msg)

    def test_equals_name_wilded(self):
        """
        Teste se equals_name retorna True ao comparar com um objeto Card
        e Names depois de setar o valor do curinga.
        """

        card = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)
        card.set_wild(FullRoyalNames.SEVEN, FullRoyalSuits.SPADES)
        other_card = Card(FullRoyalNames.SEVEN, FullRoyalSuits.SPADES)
        other_name = FullRoyalNames.SEVEN
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

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        result = card.equals_suit(other_card)
        msg = "equals_suit deve retornar True para objetos Card com suit igual"
        self.assertTrue(result, msg)

    def test_equals_suit_suits_type(self):
        """
        Teste se equals_suit retorna True ao comparar com um objeto Suits.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_suit = RoyalSuits.SPADES
        result = card.equals_suit(other_suit)
        msg = "equals_suit deve retornar True para objetos Suits igual"
        self.assertTrue(result, msg)

    def test_equals_suit_card_type_different(self):
        """
        Teste se equals_suit retorna False ao comparar com um objeto Card.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_card = Card(RoyalNames.ACE, RoyalSuits.CLUBS)
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

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other_suit = RoyalSuits.CLUBS
        result = card.equals_suit(other_suit)
        msg = "equals_suit deve retornar False para objetos Suits diferente."
        self.assertFalse(result, msg)

    def test_equals_suit_different_type(self):
        """
        Teste se equals_suit retorna False ao comparar com um objeto não-Card
        e não-Suits.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        other = "Not a Card object"
        result = card.equals_suit(other)
        msg = "equals_suit deve retornar False para objetos que não Card/Suits"
        self.assertFalse(result, msg)

    def test_equals_suit_wilded(self):
        """
        Teste se equals_suit retorna True ao comparar com um objeto Card
        e Suits depois de setar o valor do curinga.
        """

        card = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)
        card.set_wild(FullRoyalNames.SEVEN, FullRoyalSuits.SPADES)
        other_card = Card(FullRoyalNames.SEVEN, FullRoyalSuits.SPADES)
        other_name = FullRoyalSuits.SPADES
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

        card = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)
        self.assertEqual(card.name, FullRoyalNames.JOKER)
        self.assertEqual(card.suit, FullRoyalSuits.JOKER)
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)

        card.set_wild(FullRoyalNames.ACE, FullRoyalSuits.SPADES)
        self.assertEqual(card.name, FullRoyalNames.ACE)
        self.assertEqual(card.suit, FullRoyalSuits.SPADES)
        self.assertEqual(card.wild_name, FullRoyalNames.ACE)
        self.assertEqual(card.wild_suit, FullRoyalSuits.SPADES)

    def test_set_wild_name(self):
        """
        Teste se o método set_wild_name altera corretamente o name do curinga.

        Esse teste também serve para testar as propriedades name
        """

        card = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)
        self.assertEqual(card.name, FullRoyalNames.JOKER)
        self.assertIsNone(card.wild_name)

        card.set_wild_name(FullRoyalNames.ACE)
        self.assertEqual(card.name, FullRoyalNames.ACE)
        self.assertEqual(card.wild_name, FullRoyalNames.ACE)

    def test_set_wild_name_card_is_not_wild(self):
        """
        Teste se o método set_wild_name retorna um erro ao tentar alterar
        um Card não WILD.
        """

        card = Card(FullRoyalNames.KING, FullRoyalSuits.CLUBS)
        self.assertEqual(card.name, FullRoyalNames.KING)
        self.assertIsNone(card.wild_name)

        with pytest.raises(ValueError, match=''):
            card.set_wild_name(FullRoyalNames.ACE)

    def test_set_wild_suit(self):
        """
        Teste se o método set_wild_suit altera corretamente o suit do curinga.

        Esse teste também serve para testar as propriedades suit
        """

        card = Card(FullRoyalNames.JOKER, FullRoyalSuits.JOKER)
        self.assertEqual(card.suit, FullRoyalSuits.JOKER)
        self.assertIsNone(card.wild_suit)

        card.set_wild_suit(FullRoyalSuits.SPADES)
        self.assertEqual(card.suit, FullRoyalSuits.SPADES)
        self.assertEqual(card.wild_suit, FullRoyalSuits.SPADES)

    def test_set_wild_suit_card_is_not_wild(self):
        """
        Teste se o método set_wild_suit retorna um erro ao tentar alterar
        um Card não WILD.
        """

        card = Card(FullRoyalNames.ACE, FullRoyalSuits.CLUBS)
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

        card = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        expected_text = f'{RoyalSuits.HEARTS.value}{RoyalNames.ACE.value}'
        self.assertEqual(card.text, expected_text)

    def test_value_returns_correct_index(self):
        """
        Teste se a propriedade value retorna o índice correto
        para um determinado nome de carta.

        Este teste verifica se a propriedade value de uma instância de
        Card chama corretamente a função get_enum_index com o nome
        da carta e retorna o resultado.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.HEARTS)
        expected_value = get_enum_index(RoyalNames.ACE)
        self.assertEqual(card.value, expected_value)

    def test_value_valid_input(self):
        """
        Teste se a propriedade value retorna o índice enum correto
        para um nome de Card válido.
        """

        card = Card(RoyalNames.ACE, RoyalSuits.SPADES)
        self.assertEqual(card.value, 0)
