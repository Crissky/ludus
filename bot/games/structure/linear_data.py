from abc import ABC, abstractmethod
from collections.abc import Generator
from random import shuffle
from typing import List, Union

from bot.games.cards.card import Card


class LinearDataStructure(ABC):
    def __init__(self, *cards: Card):
        self.items = []

        for card in cards:
            self.push(card)

    def __iter__(self) -> Generator[Card]:
        for i in range(len(self.items)):
            yield self.items[i]

    def __getitem__(self, index: int) -> Union[Card, List[Card]]:
        return self.items[index]

    def __len__(self) -> int:
        return len(self.items)

    def shuffle(self):
        shuffle(self.items)

    @abstractmethod
    def push(self, *cards: Card):
        raise NotImplementedError('Subclasse deve implementar push.')

    @abstractmethod
    def push_bottom(self, *cards: Card):
        raise NotImplementedError('Subclasse deve implementar push_bottom')

    @abstractmethod
    def pop(self, quantity: int = 1) -> Union[Card, List[Card]]:
        raise NotImplementedError('Subclasse deve implementar pop')

    @abstractmethod
    def peek(self, quantity: int = 1) -> Union[Card, List[Card]]:
        raise NotImplementedError('Subclasse deve implementar peek')

    @abstractmethod
    def peek_bottom(self, quantity: int = 1) -> Union[Card, List[Card]]:
        raise NotImplementedError('Subclasse deve implementar peek_bottom')

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    @property
    def text_horizontal(self) -> str:
        return ' '.join([card.text for card in self])

    @property
    def text_vertical(self) -> str:
        return '\n'.join([card.text for card in self])

    @property
    def text_lazy(self) -> Generator[str]:
        return (card.text for card in self)
