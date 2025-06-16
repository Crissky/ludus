from random import randint
from typing import List
from bot.games.cards.card import Card


class BaseHand:
    def __init__(self, max_size: int = 0, *cards: Card):
        self.max_size = max_size
        self.card_list = list(cards)

    def __len__(self):
        return len(self.card_list)

    def add_card(self, card: Card, discard_index: int = -1):
        if self.max_size > 0 and len(self) >= self.max_size:
            self.discard(discard_index)
        self.card_list.append(card)

    def discard(self, index: int = -1):
        if index < 0:
            index = randint(0, len(self) - 1)
        self.card_list.pop(index)

    def play(self, *indexes: int) -> List[Card]:
        indexes = sorted(indexes, reverse=True)
        cards = []
        for index in indexes:
            popped_card = self.card_list.pop(index)
            cards.append(popped_card)
        return cards

    def peek(self, *indexes: int) -> List[Card]:
        cards = []
        for index in indexes:
            peeked_card = self.card_list[index]
            cards.append(peeked_card)
        return cards
