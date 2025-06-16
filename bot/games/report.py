from typing import List
from bot.games.player import Player


class Report:
    def __init__(self, game_id, player_list: List[Player]):
        self.game_id = game_id
        self.player_list = player_list
        self.report = {}
