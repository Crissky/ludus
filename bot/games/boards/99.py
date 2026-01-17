from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.player import Player


class NineNineBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = '💯99'
    DESCRIPTION: str = ('')

    def __init__(self, *players: Player, debug: bool = False):
        ...