from bot.games.boards.cardgame_board import CardGameBoard
from bot.games.decks.color import ColorDeck


class ColorGameBoard(CardGameBoard):
    def __init__(self, player_list: list):
        draw_pile = ColorDeck()
        super().__init__(
            name='Color',
            player_list=player_list,
            draw_pile=draw_pile,
            total_discard_pile=1,
            initial_hand_size=7,
            hand_kwargs={}
        )
