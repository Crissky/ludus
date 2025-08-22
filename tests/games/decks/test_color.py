import unittest
from bot.games.decks.color import ColorDeck
from bot.games.enums.card import ColorNames, ColorSuits


class TestColorDeck(unittest.TestCase):
    def setUp(self):
        """Configurar método para o caso de teste."""

        self.deck = ColorDeck(is_shuffle=False, total_decks=1)
        self.shuffled_deck = ColorDeck(is_shuffle=True, total_decks=1)

    def test_init_default_parameters(self):
        """Teste a inicialização do ColorDeck com parâmetros padrão."""

        deck = ColorDeck()
        self.assertIsInstance(deck, ColorDeck)
        self.assertTrue(len(deck) > 0)

    def test_init_no_shuffle(self):
        """Teste a inicialização do ColorDeck sem embaralhar."""

        deck = ColorDeck(is_shuffle=False)
        self.assertIsInstance(deck, ColorDeck)
        self.assertEqual(len(deck), 108)

    def test_init_multiple_decks(self):
        """Teste a inicialização do ColorDeck com múltiplos baralhos."""

        deck = ColorDeck(is_shuffle=False, total_decks=1)
        double_deck = ColorDeck(is_shuffle=False, total_decks=2)
        triple_deck = ColorDeck(is_shuffle=False, total_decks=3)
        self.assertEqual(len(deck), 108)
        self.assertEqual(len(double_deck), 216)
        self.assertEqual(len(triple_deck), 324)

    def test_deck_size_108_cards(self):
        """Teste se o deck possui exatamente 108 cartas."""

        self.assertEqual(len(self.deck), 108)

    def test_quantities_configuration(self):
        """Teste se as quantidades estão configuradas corretamente."""

        # Contar cartas por tipo
        zero_black_count = 0
        plus_zero_black_count = 0
        plus_four_black_count = 0
        zero_colored_count = 0
        color_suit_list = [
            ColorSuits.RED,
            ColorSuits.BLUE,
            ColorSuits.GREEN,
            ColorSuits.YELLOW
        ]
        colored_suits_count = {
            suit: 0
            for suit in color_suit_list
        }

        for card in self.deck:
            name = card.name
            suit = card.suit
            if name == ColorNames.ZERO and suit == ColorSuits.BLACK:
                zero_black_count += 1
            elif name == ColorNames.PLUS_ZERO and suit == ColorSuits.BLACK:
                plus_zero_black_count += 1
            elif name == ColorNames.PLUS_FOUR and suit == ColorSuits.BLACK:
                plus_four_black_count += 1
            elif name == ColorNames.ZERO and suit != ColorSuits.BLACK:
                zero_colored_count += 1
            elif suit in colored_suits_count:
                colored_suits_count[suit] += 1

        # Verificar quantidades esperadas
        # (ZERO, BLACK): 0
        self.assertEqual(zero_black_count, 0)
        # (PLUS_ZERO, BLACK): 4
        self.assertEqual(plus_zero_black_count, 4)
        # (PLUS_FOUR, BLACK): 4
        self.assertEqual(plus_four_black_count, 4)
        # ZERO: 1 para cada cor não-preta
        self.assertEqual(zero_colored_count, 4)

    def test_colored_suits_quantity(self):
        """Teste se cada naipe colorido tem a quantidade correta de cartas."""

        colored_suits = [
            ColorSuits.RED,
            ColorSuits.BLUE,
            ColorSuits.GREEN,
            ColorSuits.YELLOW
        ]

        for suit in colored_suits:
            suit_count = sum(1 for card in self.deck if card.suit == suit)
            # 2 cartas por nome (exceto exceções) + 1 ZERO
            self.assertEqual(suit_count, 25)

    def test_black_suits_quantity(self):
        """Teste se o naipe preto tem a quantidade correta de cartas."""

        black_count = sum(
            1 for card in self.deck if card.suit == ColorSuits.BLACK
        )
        self.assertEqual(black_count, 8)  # 4 PLUS_ZERO + 4 PLUS_FOUR

    def test_names_and_suits_types(self):
        """Teste se os nomes e naipes são dos tipos corretos."""

        self.assertEqual(self.deck.names, ColorNames)
        self.assertEqual(self.deck.suits, ColorSuits)

    def test_shuffle_parameter(self):
        """Teste se o parâmetro is_shuffle funciona corretamente."""

        deck1 = ColorDeck(is_shuffle=False)
        deck2 = ColorDeck(is_shuffle=False)

        # Dois decks não embaralhados devem ter a mesma ordem
        cards1 = [str(card) for card in deck1]
        cards2 = [str(card) for card in deck2]
        self.assertEqual(cards1, cards2)

    def test_inheritance_from_base_deck(self):
        """Teste se ColorDeck herda corretamente de BaseDeck."""

        from bot.games.decks.deck import BaseDeck
        self.assertIsInstance(self.deck, BaseDeck)

    def test_deck_methods_work(self):
        """Teste se os métodos herdados funcionam corretamente."""

        initial_size = len(self.deck)

        # Teste draw
        drawn_cards = self.deck.draw(2)
        self.assertEqual(len(drawn_cards), 2)
        self.assertEqual(len(self.deck), initial_size - 2)

        # Teste peek
        peeked_cards = self.deck.peek(1)
        self.assertEqual(len(peeked_cards), 1)
        # Tamanho não deve mudar
        self.assertEqual(len(self.deck), initial_size - 2)

    def test_main_execution_compatibility(self):
        """Teste se o código do __main__ funciona sem erros."""

        # Simula a execução do bloco __main__
        deck = ColorDeck(is_shuffle=False, total_decks=1)
        self.assertEqual(len(deck), 108)
        self.assertTrue(len(deck) == 108)
