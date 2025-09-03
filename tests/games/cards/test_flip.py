import unittest

from bot.games.cards.flip import FlipCard
from bot.games.enums.card import (
    ColorNames,
    ColorSuits,
    FlipColorNames,
    FlipColorSuits
)


class TestFlipCard(unittest.TestCase):

    def setUp(self):
        self.card = FlipCard(
            name=ColorNames.SIX,
            suit=ColorSuits.RED,
            flip_name=FlipColorNames.NINE,
            flip_suit=FlipColorSuits.ORAGE,
        )
        self.card_wild = FlipCard(
            name=ColorNames.PLUS_ZERO,
            suit=ColorSuits.BLACK,
            flip_name=FlipColorNames.NINE,
            flip_suit=FlipColorSuits.ORAGE,
        )
        self.card_flip_wild = FlipCard(
            name=ColorNames.SIX,
            suit=ColorSuits.RED,
            flip_name=FlipColorNames.PLUS_ZERO,
            flip_suit=FlipColorSuits.BLACK,
        )
        self.card_flip_wild.flip()
        self.card_double_wild = FlipCard(
            name=ColorNames.PLUS_ZERO,
            suit=ColorSuits.BLACK,
            flip_name=FlipColorNames.PLUS_ZERO,
            flip_suit=FlipColorSuits.BLACK,
        )

    def test_init(self):
        """
        Teste a inicialização de um objeto FlipCard com parâmetros válidos.
        Verifica se os atributos estão definidos corretamente
        após a inicialização.
        """

        card = self.card
        self.assertEqual(card.name, ColorNames.SIX)
        self.assertEqual(card.suit, ColorSuits.RED)
        self.assertEqual(card.flip_name, FlipColorNames.NINE)
        self.assertEqual(card.flip_suit, FlipColorSuits.ORAGE)

    def test_flip_toggles_is_flipped(self):
        """
        Teste se o método flip() alterna o atributo is_flipped.
        """

        card = self.card
        initial_state = card.is_flipped
        card.flip()
        self.assertNotEqual(card.is_flipped, initial_state)
        card.flip()
        self.assertEqual(card.is_flipped, initial_state)

    def test_set_wild_name(self):
        """
        Teste se set_wild_name muda o valor de name corretamente.
        """

        card = self.card_wild
        name = card.get_name()
        new_name = ColorNames.ZERO

        self.assertEqual(card.get_name(), name)
        card.set_wild_name(new_name)
        self.assertNotEqual(card.get_name(), name)
        self.assertEqual(card.get_name(), new_name)

    def test_set_wild_name_flip(self):
        """
        Teste se set_wild_name muda o valor flip_name corretamente.
        """

        card = self.card_flip_wild
        flip_name = card.get_flip_name()
        new_flip_name = FlipColorNames.ZERO

        self.assertEqual(card.get_flip_name(), flip_name)
        card.set_wild_name(new_flip_name)
        self.assertNotEqual(card.get_flip_name(), flip_name)
        self.assertEqual(card.get_flip_name(), new_flip_name)

    def test_set_wild_name_no_wild(self):
        """
        Teste se set_wild_name retorna uma exceção quando name não é um WILD.

        Este teste verifica se, ao tentar definir um nome curinga para uma
        carta virada com um nome que não é uma instância do tipo
        Enum correto, um erro de tipo é gerado.
        O teste garante que o método verifique corretamente o tipo
        do parâmetro "name" e gere a exceção apropriada quando
        o tipo estiver incorreto.
        """

        card = self.card
        msg_error = f'{card.suit.name} não é um valor WILD válido.'
        with self.assertRaises(ValueError) as context:
            card.set_wild_name(ColorNames.ZERO)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_name_no_wild_flip(self):
        """
        Teste se set_wild_name retorna uma exceção quando flip_name
        não é um WILD.
        """

        card = self.card
        card.flip()
        msg_error = f'{card.suit.name} não é um valor WILD válido.'
        with self.assertRaises(ValueError) as context:
            card.set_wild_name(FlipColorNames.ONE)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_name_invalid_type(self):
        """
        Teste o método set_wild_name com um tipo inválido para o
        parâmetro name.

        Isso deve gerar um TypeError.
        """

        card = self.card_wild
        new_wild_name = FlipColorNames.ZERO
        msg_error = f'name precisa ser um Enum do tipo {card.name.__class__}.'
        with self.assertRaises(TypeError) as context:
            card.set_wild_name(new_wild_name)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_name_invalid_type_flip(self):
        """
        Teste o método set_wild_name com um tipo inválido para o
        parâmetro flip_name.

        Isso deve gerar um TypeError.
        """

        card = self.card_flip_wild
        new_wild_name = ColorNames.ZERO
        msg_error = f'name precisa ser um Enum do tipo {card.name.__class__}.'
        with self.assertRaises(TypeError) as context:
            card.set_wild_name(new_wild_name)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_suit(self):
        """
        Teste se set_wild_suit muda o valor de suit corretamente.
        """

        card = self.card_wild
        suit = card.get_suit()
        new_suit = ColorSuits.YELLOW

        self.assertEqual(card.get_suit(), suit)
        card.set_wild_suit(new_suit)
        self.assertNotEqual(card.get_suit(), suit)
        self.assertEqual(card.get_suit(), new_suit)

    def test_set_wild_suit_flip(self):
        """
        Teste se set_wild_suit muda o valor flip_suit corretamente.
        """

        card = self.card_flip_wild
        flip_suit = card.get_flip_suit()
        new_flip_suit = FlipColorSuits.WHITE

        self.assertEqual(card.get_flip_suit(), flip_suit)
        card.set_wild_suit(new_flip_suit)
        self.assertNotEqual(card.get_flip_suit(), flip_suit)
        self.assertEqual(card.get_flip_suit(), new_flip_suit)

    def test_set_wild_suit_no_wild(self):
        """
        Teste se set_wild_suit retorna uma exceção quando suit não é um WILD.

        Este teste verifica se, ao tentar definir um nome curinga para uma
        carta virada com um nome que não é uma instância do tipo
        Enum correto, um erro de tipo é gerado.
        O teste garante que o método verifique corretamente o tipo
        do parâmetro "suit" e gere a exceção apropriada quando
        o tipo estiver incorreto.
        """

        card = self.card
        msg_error = f'{card.suit.name} não é um valor WILD válido.'
        with self.assertRaises(ValueError) as context:
            card.set_wild_suit(ColorSuits.YELLOW)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_suit_no_wild_flip(self):
        """
        Teste se set_wild_suit retorna uma exceção quando flip_suit
        não é um WILD.
        """

        card = self.card
        card.flip()
        msg_error = f'{card.suit.name} não é um valor WILD válido.'
        with self.assertRaises(ValueError) as context:
            card.set_wild_suit(FlipColorSuits.WHITE)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_suit_invalid_type(self):
        """
        Teste o método set_wild_suit com um tipo inválido para o
        parâmetro suit.

        Isso deve gerar um TypeError.
        """

        card = self.card_wild
        new_wild_suit = FlipColorSuits.WHITE
        msg_error = f'suit precisa ser um Enum do tipo {card.suit.__class__}.'
        with self.assertRaises(TypeError) as context:
            card.set_wild_suit(new_wild_suit)

        self.assertEqual(str(context.exception), msg_error)

    def test_set_wild_suit_invalid_type_flip(self):
        """
        Teste o método set_wild_suit com um tipo inválido para o
        parâmetro flip_suit.

        Isso deve gerar um TypeError.
        """

        card = self.card_flip_wild
        new_wild_name = ColorSuits.YELLOW
        msg_error = f'suit precisa ser um Enum do tipo {card.suit.__class__}.'
        with self.assertRaises(TypeError) as context:
            card.set_wild_suit(new_wild_name)

        self.assertEqual(str(context.exception), msg_error)

    def test_unset_wild_1(self):
        """
        Teste se unset_wild reseta os valores de wild_name e wild_suit
        corretamente.
        """

        card = self.card_wild
        new_name = ColorNames.ZERO
        new_suit = ColorSuits.YELLOW
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)
        self.assertNotEqual(card.wild_name, new_name)
        self.assertNotEqual(card.wild_suit, new_suit)

        card.set_wild(name=new_name, suit=new_suit)
        self.assertEqual(card.wild_name, new_name)
        self.assertEqual(card.wild_suit, new_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)
        self.assertEqual(card.name, new_name)
        self.assertEqual(card.suit, new_suit)

        card.unset_wild()
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)

    def test_unset_wild_2(self):
        """
        Teste se unset_wild reseta os valores de flip_wild_name e
        flip_wild_suit corretamente.
        """

        card = self.card_flip_wild
        new_flip_name = FlipColorNames.ZERO
        new_flip_suit = FlipColorSuits.WHITE
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)
        self.assertNotEqual(card.flip_wild_name, new_flip_name)
        self.assertNotEqual(card.flip_wild_suit, new_flip_suit)

        card.set_wild(name=new_flip_name, suit=new_flip_suit)
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertEqual(card.flip_wild_name, new_flip_name)
        self.assertEqual(card.flip_wild_suit, new_flip_suit)
        self.assertEqual(card.name, new_flip_name)
        self.assertEqual(card.suit, new_flip_suit)

        card.unset_wild()
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)

    def test_unset_wild_3(self):
        """
        Teste se unset_wild reseta os valores de wild_name, wild_suit,
        flip_wild_name e flip_wild_suit corretamente.
        """

        card = self.card_double_wild
        new_name = ColorNames.ZERO
        new_suit = ColorSuits.YELLOW
        new_flip_name = FlipColorNames.ZERO
        new_flip_suit = FlipColorSuits.WHITE
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)
        self.assertNotEqual(card.wild_name, new_name)
        self.assertNotEqual(card.wild_suit, new_suit)

        card.set_wild(name=new_name, suit=new_suit)
        self.assertIsNotNone(card.wild_name)
        self.assertIsNotNone(card.wild_suit)
        self.assertEqual(card.wild_name, new_name)
        self.assertEqual(card.wild_suit, new_suit)
        self.assertEqual(card.name, new_name)
        self.assertEqual(card.suit, new_suit)

        card.flip()
        card.set_wild(name=new_flip_name, suit=new_flip_suit)
        self.assertIsNotNone(card.wild_name)
        self.assertIsNotNone(card.wild_suit)
        self.assertIsNotNone(card.flip_wild_name)
        self.assertIsNotNone(card.flip_wild_suit)
        self.assertEqual(card.flip_wild_name, new_flip_name)
        self.assertEqual(card.flip_wild_suit, new_flip_suit)
        self.assertEqual(card.name, new_flip_name)
        self.assertEqual(card.suit, new_flip_suit)

        card.unset_wild()
        self.assertIsNone(card.wild_name)
        self.assertIsNone(card.wild_suit)
        self.assertIsNone(card.flip_wild_name)
        self.assertIsNone(card.flip_wild_suit)

    def test_get_name(self):
        """
        Teste se o método get_name retorna o valor correto para name.
        """

        card = self.card_wild
        self.assertEqual(card.get_name(), card.real_name)
        self.assertIsNone(card.wild_name)
        card.set_wild_name(ColorNames.ZERO)
        self.assertEqual(card.get_name(), card.wild_name)
        self.assertIsNotNone(card.wild_name)

    def test_get_flip_name(self):
        """
        Teste se o método get_flip_name retorna o valor correto para name.
        """

        card = self.card_flip_wild
        self.assertEqual(card.get_flip_name(), card.flip_name)
        self.assertIsNone(card.flip_wild_name)
        card.set_wild_name(FlipColorNames.ZERO)
        self.assertEqual(card.get_flip_name(), card.flip_wild_name)
        self.assertIsNotNone(card.flip_wild_name)

    def test_get_suit(self):
        """
        Teste se o método get_suit retorna o valor correto para suit.
        """

        card = self.card_wild
        self.assertEqual(card.get_suit(), card.real_suit)
        self.assertIsNone(card.wild_suit)
        card.set_wild_suit(ColorSuits.YELLOW)
        self.assertEqual(card.get_suit(), card.wild_suit)
        self.assertIsNotNone(card.wild_suit)

    def test_get_flip_suit(self):
        """
        Teste se o método get_flip_suit retorna o valor correto para suit.
        """

        card = self.card_flip_wild
        self.assertEqual(card.get_flip_suit(), card.flip_suit)
        self.assertIsNone(card.flip_wild_suit)
        card.set_wild_suit(FlipColorSuits.WHITE)
        self.assertEqual(card.get_flip_suit(), card.flip_wild_suit)
        self.assertIsNotNone(card.flip_wild_suit)

    def test_full_text_returns_formatted_string(self):
        """
        Teste se a propriedade full_text retorna uma string formatada
        corretamente contendo o nome da carta, naipe, nome da carta flipada
        e naipe da carta flipada.
        """
        card = self.card
        name = card.get_name().value
        suit = card.get_suit().value
        flip_name = card.get_flip_name().value
        flip_suit = card.get_flip_suit().value
        expected_full_text = f'{suit}{name} | {flip_suit}{flip_name}'

        self.assertEqual(card.full_text, expected_full_text)

    def test_name(self):
        """
        Teste se a propriedade name retorna o nome da carta corretamente.
        """

        card = self.card
        name = card.get_name()
        flip_name = card.get_flip_name()
        self.assertEqual(card.name, name)
        card.flip()
        self.assertEqual(card.name, flip_name)

    def test_suit(self):
        """
        Teste se a propriedade suit retorna o nome da carta corretamente.
        """

        card = self.card
        suit = card.get_suit()
        flip_suit = card.get_flip_suit()
        self.assertEqual(card.suit, suit)
        card.flip()
        self.assertEqual(card.suit, flip_suit)
