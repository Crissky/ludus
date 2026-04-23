import logging

from bot.games.boards.board import BaseBoard
from bot.games.player import Player


logger = logging.getLogger(__name__)


class WarfareBoard(BaseBoard):
    def __init__(
        self,
        *players: Player,
        min_total_players: int = 3,
        max_total_players: int = 6,
        debug: bool = False,
    ):
        super().__init__(
            *players,
            min_total_players=min_total_players,
            max_total_players=max_total_players,
            debug=debug,
        )
