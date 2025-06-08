from collections.abc import Generator
from enum import Enum
from typing import List, Union

from bot.games.cards.card import Card
from bot.games.structure.stack import Stack


class BaseDeck:
    def __init__(
        self,
        names: Enum,
        suits: Enum,
        quantity: dict = None,
        shuffle: bool = True
    ):
        self.card_list = Stack()
        if quantity is None:
            quantity = {suit: 1 for suit in suits}

        for name in names:
            for suit in suits:
                name_suit_qty = quantity.get((name, suit))
                name_qty = quantity.get(name)
                suit_qty = quantity.get(suit)
                if isinstance(name_suit_qty, int):
                    card_qty = name_suit_qty
                elif isinstance(name_qty, int):
                    card_qty = name_qty
                else:
                    card_qty = suit_qty
                for _ in range(card_qty):
                    self.card_list.push(Card(name, suit))

        if shuffle is True:
            self.shuffle()

    def __iter__(self) -> Generator[Card]:
        return iter(self.card_list)

    def __len__(self) -> int:
        return len(self.card_list)

    def __getitem__(self, index) -> Union[Card, List[Card]]:
        return self.card_list[index]

    def __str__(self) -> str:
        return self.card_list.text_horizontal

    def draw(self, quantity: int) -> Union[Card, List[Card]]:
        return self.card_list.pop(quantity=quantity)

    def peek(self, quantity: int) -> Union[Card, List[Card]]:
        return self.card_list.peek(quantity=quantity)

    def shuffle(self):
        self.card_list.shuffle()
