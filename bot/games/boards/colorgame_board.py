from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.decks.color import ColorDeck
from bot.games.player import Player


class ColorsGameBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = 'Colors'
    DESCRIPTION: str = None

    def __init__(self, *players: Player):
        draw_pile = ColorDeck()
        super().__init__(
            *players,
            draw_pile=draw_pile,
            total_discard_pile=1,
            initial_hand_size=7,
            hand_kwargs={}
        )
