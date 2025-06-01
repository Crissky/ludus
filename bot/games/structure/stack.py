from typing import Generator

from bot.games.cards.card import Card
from bot.games.structure.linear_data import LinearDataStructure


class Stack(LinearDataStructure):
    def __iter__(self) -> Generator:
        for i in range((len(self.items) - 1), -1, -1):
            yield self.items[i]

    def push(self, card: Card):
        self.items.append(card)

    def pop(self) -> Card:
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def peek(self) -> Card:
        if not self.is_empty():
            return self.items[-1]
