from bot.games.cards.card import Card
from bot.games.structure.linear_data import LinearDataStructure


class Queue(LinearDataStructure):
    def push(self, card: Card):
        self.items.append(card)

    def pop(self) -> Card:
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None

    def peek(self) -> Card:
        if not self.is_empty():
            return self.items[0]

