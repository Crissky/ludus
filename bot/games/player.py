from collections.abc import Generator

from telegram import User
from bot.games.cards.card import Card
from bot.games.hands.hand import BaseHand


class Player:
    def __init__(
        self,
        player_id: str = None,
        name: str = None,
        user: User = None,
        hand: BaseHand = None,
        message_id: int = None,
    ):
        if ((player_id is None or name is None) and user is None):
            raise ValueError('player_id e name ou user devem ser informados.')

        if player_id and name:
            self.id = str(player_id)
            self.name = name
        else:
            self.id = str(user.id)
            self.name = user.name

        if hand is None:
            hand = BaseHand()
        self.hand = hand

        if not isinstance(message_id, int):
            raise TypeError('message_id precisa ser do tipo int.')
        self.message_id = message_id

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __iter__(self) -> Generator[Card]:
        yield from self.hand

    def __getitem__(self, index):
        return self.hand[index]

    def __setitem__(self, index, value):
        self.hand[index] = value

    def __len__(self):
        return len(self.hand)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'Player(id={self.id}, '
            f'name={self.name}, '
            f'message_id={self.message_id}'
            ')'
        )

    def set_hand(self, hand: BaseHand):
        if isinstance(hand, BaseHand):
            self.hand = hand
        else:
            raise TypeError('hand precisa ser do tipo BaseHand.')

    def set_message_id(self, message_id: int):
        if not isinstance(message_id, int):
            raise TypeError('message_id precisa ser do tipo int.')

        self.message_id = message_id

    @property
    def user_id(self):
        return self.id
    player_id = user_id

    @property
    def user_name(self):
        return self.name
