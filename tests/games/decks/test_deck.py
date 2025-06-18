from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.stack import Stack
from collections.abc import Generator
import unittest


class TestDeck(unittest.TestCase):
    def setUp(self):
        """
        Configurar método para o caso de teste.
        Este método é chamado antes de cada método de teste.
        """

        self.deck = BaseDeck(names=RoyalNames, suits=RoyalSuits, shuffle=False)
        self.empty_deck = BaseDeck()
        self.card_last = Card(RoyalNames.ACE, RoyalSuits.CLUBS)
        self.card0 = Card(RoyalNames.KING, RoyalSuits.SPADES)
        self.card1 = Card(RoyalNames.KING, RoyalSuits.HEARTS)
        self.card2 = Card(RoyalNames.KING, RoyalSuits.DIAMONDS)
        self.card3 = Card(RoyalNames.KING, RoyalSuits.CLUBS)

    def test_init_quantities_1(self):
        """
        Teste a inicialização do BaseDeck com quantidades personalizadas.

        Todos os Names de um Suit.
        """

        quantities = {
            RoyalSuits.CLUBS: 0,
            RoyalSuits.DIAMONDS: 0,
            RoyalSuits.HEARTS: 0,
            RoyalSuits.SPADES: 1,
        }

        deck = BaseDeck(
            RoyalNames,
            RoyalSuits,
            quantities=quantities,
            shuffle=False
        )

        self.assertEqual(len(deck), len(RoyalNames))
        for card, name in zip(deck, reversed(RoyalNames)):
            self.assertEqual(card.suit, RoyalSuits.SPADES)
            self.assertEqual(card.name, name)

    def test_init_quantities_2(self):
        """
        Teste a inicialização do BaseDeck com quantidades personalizadas.

        Um único Name de todos os Suits.
        """

        quantities = {
            RoyalSuits.CLUBS: 0,
            RoyalSuits.DIAMONDS: 0,
            RoyalSuits.HEARTS: 0,
            RoyalSuits.SPADES: 0,
            RoyalNames.ACE: 1,
        }

        deck = BaseDeck(
            RoyalNames,
            RoyalSuits,
            quantities=quantities,
            shuffle=False
        )

        self.assertEqual(len(deck), len(RoyalSuits))
        for card, suit in zip(deck, reversed(RoyalSuits)):
            self.assertEqual(card.suit, suit)
            self.assertEqual(card.name, RoyalNames.ACE)

    def test_init_quantities_3(self):
        """
        Teste a inicialização do BaseDeck com quantidades personalizadas.

        Um único Name e Suit.
        """

        quantities = {
            (RoyalNames.ACE, RoyalSuits.SPADES): 1,
            RoyalSuits.CLUBS: 0,
            RoyalSuits.DIAMONDS: 0,
            RoyalSuits.HEARTS: 0,
            RoyalSuits.SPADES: 0,
        }

        deck = BaseDeck(
            RoyalNames,
            RoyalSuits,
            quantities=quantities,
            shuffle=False
        )

        self.assertEqual(len(deck), 1)
        for card in deck:
            self.assertEqual(card.suit, RoyalSuits.SPADES)
            self.assertEqual(card.name, RoyalNames.ACE)

    def test_init_no_quantities(self):
        """
        Teste a inicialização do BaseDeck quando quantity for None.
        Deve criar uma card para cada combinação de Name x Suit
        """

        deck = BaseDeck(names=RoyalNames, suits=RoyalSuits, shuffle=False)
        self.assertEqual(len(deck), len(RoyalNames) * len(RoyalSuits))

    def test_init_no_names_suits(self):
        """
        Teste a inicialização do BaseDeck quando names ou suits for None.
        Deve criar um deck vazio.
        """

        deck1 = BaseDeck(shuffle=False)
        deck2 = BaseDeck(names=RoyalNames, shuffle=False)
        deck3 = BaseDeck(suits=RoyalSuits, shuffle=False)
        self.assertEqual(len(deck1), 0)
        self.assertEqual(len(deck2), 0)
        self.assertEqual(len(deck3), 0)
        self.assertIsInstance(deck1.card_stack, Stack)
        self.assertIsInstance(deck2.card_stack, Stack)
        self.assertIsInstance(deck3.card_stack, Stack)

    def test_init_total_decks(self):
        """Teste a inicialização do BaseDeck com total_decks maior que 1.
        """

        total_decks1 = 2
        total_decks2 = 10
        size_deck = len(RoyalNames) * len(RoyalSuits)
        deck1 = BaseDeck(RoyalNames, RoyalSuits, total_decks=total_decks1)
        deck2 = BaseDeck(RoyalNames, RoyalSuits, total_decks=total_decks2)

        self.assertEqual(len(deck1), size_deck * total_decks1)
        self.assertEqual(len(deck2), size_deck * total_decks2)

    def test_iter_empty_deck(self):
        """
        Teste o método __iter__ com um deck vazio para garantir que
        ele trate esse caso extremo corretamente.
        """

        items = list(self.empty_deck)
        msg = "Expected an empty iteration for an empty deck"
        self.assertEqual(len(items), 0, msg)

    def test_iter_returns_iterator(self):
        """
        Teste se o método __iter__ do BaseDeck retorna um iterador
        de objetos Card.
        """

        iterator = iter(self.deck)

        self.assertIsInstance(iterator, Generator)
        first_card = next(iterator)
        self.assertIsInstance(first_card, Card)
        self.assertEqual(first_card.name, RoyalNames.KING)
        self.assertEqual(first_card.suit, RoyalSuits.SPADES)

    def test_len(self):
        """
        Teste o método __len__ com um deck vazio.
        Isso testa o caso extremo em que o deck não tem cartas.
        """

        self.assertEqual(len(self.deck), len(RoyalNames) * len(RoyalSuits))

    def test_len_empty_deck(self):
        """
        Teste o método __len__ com um deck vazio.
        Isso testa o caso extremo em que o deck não tem cartas.
        """

        self.assertEqual(len(self.empty_deck), 0)

    def test_getitem(self):
        """
        Teste se o método __getitem__ do BaseDeck retorna a card
        correta no índice fornecido.
        """

        self.assertEqual(self.deck[0], self.card0)
        self.assertEqual(self.deck[1], self.card1)
        self.assertEqual(self.deck[2], self.card2)
        self.assertEqual(self.deck[3], self.card3)

    def test_getitem_out_of_bounds_index(self):
        """
        Teste o método __getitem__ com um índice fora dos limites.
        Este teste verifica se acessar um índice além do tamanho do deck
        gera um IndexError.
        """

        with self.assertRaises(IndexError):
            _ = self.deck[len(self.deck)]

    def test_str_returns_card_stack_text_horizontal(self):
        """
        Teste se o método __str__ retorna a representação
        text_horizontal da lista de cartas.
        """

        expected_str = self.deck.card_stack.text_horizontal
        assert str(self.deck) == expected_str

    def test_repr_1(self):
        """
        Teste se o método __repr__ do BaseDeck retorna uma representação
        de string contendo o nome da classe e a representação de
        texto horizontal da lista de cartões.
        """

        expected_repr = (
            f"{self.deck.__class__.__name__}"
            f"({self.deck.card_stack.text_horizontal})"
        )
        self.assertEqual(repr(self.deck), expected_repr)

    def test_draw_single_card(self):
        """
        Teste a compra de uma única card do deck.

        Este teste verifica se:
        1. O método draw retorna um único objeto Card quando a quantidade é 1.
        2. A card comprada é removida do deck.
        3. O tamanho do deck diminui em 1 após a retirada.
        """

        initial_size = len(self.deck)
        drawn_card = self.deck.draw(1)

        self.assertIsInstance(drawn_card, Card)
        self.assertEqual(len(self.deck), initial_size - 1)
        self.assertNotIn(drawn_card, self.deck)

    def test_draw_empty_deck(self):
        """
        Teste a compra de um deck vazio.

        Este teste verifica se a tentativa de compra de um deck vazio
        não gera um IndexError e retorna None.
        """

        self.assertIsNone(self.empty_deck.draw(quantity=1))

    def test_draw_more_cards_than_available(self):
        """
        Teste comprando mais cartas do que as disponíveis no deck.

        Este teste verifica se tentar comprar mais cartas do que
        as presentes no deck retorna uma lista com as cartas disponíveis no
        deck.
        """

        initial_size = len(self.deck)
        drawed_cards = self.deck.draw(initial_size + 1)
        self.assertIsInstance(drawed_cards, list)
        self.assertEqual(len(self.deck), 0)
        self.assertGreater(initial_size, len(self.deck))
        for card in drawed_cards:
            self.assertIsInstance(card, Card)
            self.assertNotIn(card, self.deck)

    def test_draw_negative_quantity(self):
        """Teste comprando uma quantidade de cartas menor que 1.
        """

        initial_size = len(self.deck)
        drawed_cards1 = self.deck.draw(0)
        drawed_cards2 = self.deck.draw(-1)
        self.assertIsNone(drawed_cards1)
        self.assertIsNone(drawed_cards2)
        self.assertEqual(len(self.deck), initial_size)

    def test_peek_top_card(self):
        """Teste se peek(1) retorna a card do topo do deck sem removê-la.
        """

        initial_size = len(self.deck)
        peeked_card = self.deck.peek(1)
        self.assertIsInstance(peeked_card, Card)
        self.assertEqual(peeked_card, self.deck[0])
        self.assertEqual(len(self.deck), initial_size)

    def test_peek_quantity_exceeds_deck_size(self):
        """
        Teste se o método peek retorna todas as cartas do deck
        quando a quantidade excede o tamanho do deck.
        """

        initial_size = len(self.deck)
        result = self.deck.peek(initial_size + 1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), initial_size)
        for card in result:
            self.assertIsInstance(card, Card)
            self.assertIn(card, self.deck)

    def test_peek_zero_quantity(self):
        """
        Teste se o método peek retorna None quando recebe uma
        quantidade igual a zero.
        """

        result = self.deck.peek(0)
        self.assertIsNone(result)

    def test_peek_negative_quantity(self):
        """
        Teste se o método peek retorna None quando recebe uma
        quantidade negativa.
        """

        peeked_cards1 = self.deck.peek(0)
        peeked_cards2 = self.deck.peek(-1)
        self.assertIsNone(peeked_cards1)
        self.assertIsNone(peeked_cards2)

    def test_shuffle_randomizes_card_order(self):
        """
        Teste se o método de embaralhamento randomiza
        a ordem das cartas no deck.

        Este teste cria um deck, registra sua ordem inicial, embaralha-o
        e então verifica se a ordem mudou. Embora haja uma pequena
        chance de o embaralhamento resultar na mesma ordem,
        é altamente improvável.
        """

        initial_order = [card for card in self.deck]

        self.deck.shuffle()
        shuffled_order = [card for card in self.deck]
        self.assertNotEqual(initial_order, shuffled_order)

    def test_shuffle_empty_deck(self):
        """
        Teste embaralhar um deck vazio para garantir que isso
        não gere uma exceção.
        """

        self.empty_deck.shuffle()

    def test_add_single_card(self):
        """
        Teste adicionando uma única card ao deck.

        Este teste verifica se:
        1. Uma única card pode ser adicionada ao deck.
        2. O tamanho do deck aumenta em 1 após a adição da card.
        3. A card adicionada está presente no deck.
        """

        deck = self.deck
        initial_size = len(deck)
        new_card = self.card0

        deck.add(new_card)

        self.assertEqual(len(deck), initial_size + 1)
        self.assertEqual(deck[0], new_card)
        self.assertIn(new_card, deck)

    def test_add_multiple_cards(self):
        """
        Teste adicionando uma múltiplas cards ao deck.

        Este teste verifica se:
        1. Uma única card pode ser adicionada ao deck.
        2. O tamanho do deck aumenta em 1 após a adição da card.
        3. A card adicionada está presente no deck.
        """

        deck = self.empty_deck
        initial_size = len(deck)
        new_cards = [self.card0, self.card1, self.card2]

        deck.add(self.card3)
        deck.add(*new_cards)

        self.assertEqual(len(deck), initial_size + 4)
        self.assertEqual(deck.draw(), new_cards[2])
        self.assertEqual(deck.draw(), new_cards[1])
        self.assertEqual(deck.draw(), new_cards[0])
        self.assertEqual(deck.draw(), self.card3)

    def test_add_bottom_single_card(self):
        """
        Teste adicionando uma única card ao deck na parte inferior.

        Este teste verifica se:
        1. Uma única card pode ser adicionada ao deck na parte inferior.
        2. O tamanho do deck aumenta em 1 após a adição da card.
        3. A card adicionada está presente no deck.
        """

        deck = self.deck
        initial_size = len(deck)
        new_card = self.card0

        deck.add_bottom(new_card)

        self.assertEqual(len(deck), initial_size + 1)
        self.assertEqual(deck[-1], new_card)
        self.assertIn(new_card, deck)
    
    def test_add_bottom_multiple_cards(self):
        """
        Teste adicionando uma múltiplas cards ao deck na parte inferior.

        Este teste verifica se:
        1. Uma única card pode ser adicionada ao deck na parte inferior.
        2. O tamanho do deck aumenta em 1 após a adição da card.
        3. A card adicionada está presente no deck.
        """

        deck = self.empty_deck
        initial_size = len(deck)
        new_cards = [self.card0, self.card1, self.card2]

        deck.add(self.card3)
        deck.add_bottom(*new_cards)

        self.assertEqual(len(deck), initial_size + 4)
        self.assertEqual(deck.draw(), self.card3)
        self.assertEqual(deck.draw(), new_cards[2])
        self.assertEqual(deck.draw(), new_cards[1])
        self.assertEqual(deck.draw(), new_cards[0])