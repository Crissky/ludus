from typing import List
from bot.games.player import Player


class Report:
    def __init__(
        self,
        game_id: int,
        player: Player,
        action: str,
        turn: int,
    ):
        self.game_id = game_id
        self.player = player
        self.action = action
        self.turn = turn

    def __str__(self):
        return f'{self.game_id}({self.turn}) - {self.player}: {self.action}'

    def __repr__(self):
        return f'Report({self})'
