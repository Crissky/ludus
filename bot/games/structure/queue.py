from typing import List, Union
from bot.games.cards.card import Card
from bot.games.structure.linear_data import LinearDataStructure


class Queue(LinearDataStructure):
    def push(self, *cards: Card):
        self.items.extend(cards)

    def push_botton(self, *cards: Card):
        self.items = list(cards) + self.items

    def pop(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if quantity == 1 and not self.is_empty:
            return self.items.pop(0)
        elif quantity > 1 and not self.is_empty:
            popped_items = self.items[:quantity]
            self.items = self.items[quantity:]
            return popped_items
        else:
            return None

    def peek(self, quantity: int = 1) -> Union[Card, List[Card]]:
        if quantity == 1 and not self.is_empty:
            return self.items[0]
        elif quantity > 1 and not self.is_empty:
            return self.items[:quantity]
        else:
            return None
