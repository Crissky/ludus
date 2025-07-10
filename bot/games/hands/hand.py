from collections.abc import Generator
from random import randint
from typing import List
from bot.games.cards.card import Card


class BaseHand:
    def __init__(self, max_size: int = 0, *cards: Card):
        self.max_size = max_size
        self.card_list = []

        self.add_card(*cards)

    def __getitem__(self, index: int) -> Card:
        return self.card_list[index]

    def __setitem__(self, index: int, value: Card):
        self.card_list[index] = value

    def __iter__(self) -> Generator[Card]:
        yield from self.card_list

    def __len__(self):
        return len(self.card_list)

    def __str__(self):
        return ', '.join((card.text for card in self.card_list))

    def __repr__(self):
        return f'Hand({self.card_list})'

    def add_card(
        self,
        *cards: Card,
        discard_index: int = -1
    ) -> List[Card]:
        discarded_card_list = []
        if len(self) >= self.max_size and self.max_size > 0:
            quantity = len(self) + len(cards) - self.max_size
            discarded_card_list = self.discard(discard_index, quantity)

        if isinstance(cards, Card):
            cards = [cards]

        for card in cards:
            if not isinstance(card, Card):
                raise TypeError(f"Espera um Card, obteve {type(card)}({card})")

            self.card_list.append(card)

        return discarded_card_list

    def discard(self, index: int = -1, quantity: int = 1) -> List[Card]:
        card_list = []
        for _ in range(quantity):
            if index < 0 or quantity > 1:
                index = randint(0, len(self) - 1)

            if len(self) > 0:
                card = self.card_list.pop(index)
                card_list.append(card)
            else:
                break

        return card_list

    def play(self, *indexes: int) -> List[Card]:
        cards = []
        indexes = sorted(indexes, reverse=True)
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

    def sort(self):
        self.card_list.sort()

    @property
    def is_empty(self) -> bool:
        return len(self) == 0
