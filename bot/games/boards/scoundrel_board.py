from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.decks.scoundrel import ScoundrelDeck
from bot.games.player import Player


class ScoundrelBoard(BaseCardGameBoard):
    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = ScoundrelDeck(is_shuffle=False)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=2,
            initial_hand_size=4,
            hand_kwargs={'max_size': 4},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.hp = 20
