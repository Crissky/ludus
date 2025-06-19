from typing import Generator
from bot.games.cards.card import Card
from bot.games.hands.hand import BaseHand


class Player:
    def __init__(self, id: str, name: str, hand: BaseHand = None):
        self.id = str(id)
        self.name = name
        if hand is None:
            hand = BaseHand()
        self.hand = hand

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __init__(self) -> Generator[Card]:
        yield from self.hand

    def __getitem__(self, index):
        return self.hand[index]

    def __setitem__(self, index, value):
        self.hand[index] = value

    def __len__(self):
        if self.hand is None:
            return 0
        return len(self.hand)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Player(id={self.id}, name={self.name})'

    def set_hand(self, hand: BaseHand):
        if isinstance(hand, BaseHand):
            self.hand = hand
        else:
            raise TypeError('hand precisa ser do tipo BaseHand.')

    @property
    def user_id(self):
        return self.id
    player_id = user_id

    @property
    def user_name(self):
        return self.name
