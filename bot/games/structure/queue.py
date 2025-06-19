from typing import List, Union
from bot.games.cards.card import Card
from bot.games.structure.linear_data import LinearDataStructure


class Queue(LinearDataStructure):
    def push(self, *cards: Card):
        for card in cards:
            if not isinstance(card, Card):
                raise TypeError(f"Espera um Card, obteve {type(card)}({card})")
            self.items.append(card)

    def push_bottom(self, *cards: Card):
        for card in reversed(cards):
            if not isinstance(card, Card):
                raise TypeError(f"Espera um Card, obteve {type(card)}({card})")
            self.items.insert(0, card)

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

    def peek_bottom(self, quantity=1):
        if quantity == 1 and not self.is_empty:
            return self.items[-1]
        elif quantity > 1 and not self.is_empty:
            return self.items[-quantity:]
        else:
            return None
