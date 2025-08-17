import unittest
from unittest.mock import MagicMock

from bot.games.structure.linear_data import LinearDataStructure
from bot.games.cards.card import Card


class ConcreteLinearData(LinearDataStructure):
    def push(self, *cards: Card):
        self.items.extend(cards)

    def push_bottom(self, *cards: Card):
        for card in reversed(cards):
            self.items.insert(0, card)

    def pop(self, quantity: int = 1):
        if quantity == 1:
            return self.items.pop()
        return [self.items.pop() for _ in range(quantity)]

    def peek(self, quantity: int = 1):
        if quantity == 1:
            return self.items[-1]
        return self.items[-quantity:]

    def peek_bottom(self, quantity: int = 1):
        if quantity == 1:
            return self.items[0]
        return self.items[:quantity]
