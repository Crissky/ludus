from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.stack import Stack
from collections.abc import Generator
from enum import Enum
from itertools import product
from typing import List, Union
from typing import Union, List
import pytest
import unittest


class TestDeck(unittest.TestCase):
    def setUp(self):
        """
        Configurar método para o caso de teste.
        Este método é chamado antes de cada método de teste.
        """

        self.deck = BaseDeck(names=RoyalNames, suits=RoyalSuits, shuffle=False)
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
            RoyalSuits.SPADES: 1,
            RoyalSuits.HEARTS: 0,
            RoyalSuits.DIAMONDS: 0,
            RoyalSuits.CLUBS: 0,
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
            RoyalSuits.SPADES: 0,
            RoyalSuits.HEARTS: 0,
            RoyalSuits.DIAMONDS: 0,
            RoyalSuits.CLUBS: 0,
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

    def test_init_no_quantities(self):
        """
        Teste a inicialização do BaseDeck quando quantity for None.
        Deve criar uma carta para cada combinação de Name x Suit
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
        self.assertIsInstance(deck1.card_list, Stack)
        self.assertIsInstance(deck2.card_list, Stack)
        self.assertIsInstance(deck3.card_list, Stack)

    def test_iter_empty_deck(self):
        """
        Teste o método __iter__ com um deck vazio para garantir que
        ele trate esse caso extremo corretamente.
        """

        empty_deck = BaseDeck()

        items = list(empty_deck)
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

        empty_deck = BaseDeck()
        self.assertEqual(len(empty_deck), 0)

    def test_getitem(self):
        """
        Teste se o método __getitem__ do BaseDeck retorna a carta
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

    def test_repr_1(self):
        """
        Teste se o método __repr__ do BaseDeck retorna uma representação
        de string contendo o nome da classe e a representação de
        texto horizontal da lista de cartões.
        """

        expected_repr = (
            f"{self.deck.__class__.__name__}"
            f"({self.deck.card_list.text_horizontal})"
        )
        self.assertEqual(repr(self.deck), expected_repr)
