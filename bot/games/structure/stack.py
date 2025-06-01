from typing import Generator, List, Union

from bot.games.cards.card import Card
from bot.games.structure.linear_data import LinearDataStructure


class Stack(LinearDataStructure):
    def __iter__(self) -> Generator:
        for i in range((len(self.items) - 1), -1, -1):
            yield self.items[i]

    def push(self, card: Card):
        self.items.append(card)

    def pop(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if quantity == 1:
            if not self.is_empty():
                return self.items.pop()
        elif quantity > 1:
            popped_items = self.items[-quantity:]
            self.items = self.items[:-quantity]
            return popped_items
        else:
            return None

    def peek(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if not self.is_empty():
            return self.items[-1] if quantity == 1 else self.items[-quantity:]
        else:
            return None
