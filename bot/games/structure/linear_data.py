from abc import abstractmethod
from random import shuffle
from typing import Generator, List, Union

from bot.games.cards.card import Card


class LinearDataStructure:
    def __init__(self, *args: Card):
        self.items = list(args)

    def __iter__(self) -> Generator:
        for i in range(len(self.items)):
            yield self.items[i]

    def __len__(self) -> int:
        return len(self.items)

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def shuffle(self):
        shuffle(self.items)

    @abstractmethod
    def push(self, card: Card):
        pass

    @abstractmethod
    def pop(self, quantity: int = 1) -> Union[Card, List[Card]]:
        pass

    @abstractmethod
    def peek(self, quantity: int = 1) -> Union[Card, List[Card]]:
        pass

    @property
    def text_horizontal(self) -> str:
        return ' '.join([card.text for card in self.items])

    @property
    def text_vertical(self) -> str:
        return '\n'.join([card.text for card in self.items])

    @property
    def text_lazy(self) -> Generator:
        return (card.text for card in self.items)
