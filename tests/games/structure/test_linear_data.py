from bot.games.cards.card import Card
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.structure.linear_data import LinearDataStructure
from typing import Generator
import pytest
import random
import unittest

class TestLinearData(unittest.TestCase):

    def test_init_with_multiple_cards(self):
        """
        Teste o método __init__ de LinearDataStructure com vários objetos Card.
        Verifique se o atributo items foi inicializado corretamente com
        os cards fornecidos.
        """

        card1 = Card(RoyalSuits.HEARTS, RoyalNames.ACE)
        card2 = Card(RoyalSuits.SPADES, RoyalNames.KING)
        card3 = Card(RoyalSuits.DIAMONDS, RoyalNames.QUEEN)

        linear_data = LinearDataStructure(card1, card2, card3)

        assert len(linear_data.items) == 3
        assert linear_data[0] == card1
        assert linear_data[1] == card2
        assert linear_data[2] == card3
