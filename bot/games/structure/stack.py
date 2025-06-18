from collections.abc import Generator
from typing import List, Union

from bot.games.cards.card import Card
from bot.games.structure.linear_data import LinearDataStructure


class Stack(LinearDataStructure):
    def __iter__(self) -> Generator[Card]:
        yield from reversed(self.items)

    def __getitem__(self, index: int) -> Union[Card, List[Card]]:
        reversed_items = reversed(self.items)
        reversed_items = list(reversed_items)

        return reversed_items[index]

    def push(self, *cards: Card):
        self.items.extend(cards)

    def push_botton(self, *cards: Card):
        self.items = list(cards) + self.items

    def pop(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if quantity == 1 and not self.is_empty:
            return self.items.pop()
        elif quantity > 1 and not self.is_empty:
            popped_items = reversed(self.items[-quantity:])
            self.items = self.items[:-quantity]
            return list(popped_items)
        else:
            return None

    def peek(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if quantity == 1 and not self.is_empty:
            return self.items[-1]
        elif quantity > 1 and not self.is_empty:
            peeked_items = reversed(self.items[-quantity:])
            return list(peeked_items)
        else:
            return None

    def peek_bottom(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if quantity == 1 and not self.is_empty:
            return self.items[0]
        elif quantity > 1 and not self.is_empty:
            return self.items[:quantity]
        else:
            return None
