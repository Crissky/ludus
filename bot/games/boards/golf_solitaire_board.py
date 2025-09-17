from typing import List

from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.card import Card
from bot.games.decks.royal import RoyalDeck
from bot.games.player import Player


class GolfSolitaireBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = '🏌️‍♂️Golf Solitaire'
    DESCRIPTION: str = ('')

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = RoyalDeck()
        super().__init__(
            draw_pile,
            *players,
            is_shuffle_deck=True,
            total_discard_pile=1,
            discard_at_start=True,
            initial_hand_size=0,
            hand_kwargs={'max_size': 0},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.enemy = Player(player_id='0000000000', name='Solitaire')
        self.board = []

        self.debug_attr_list.extend([
            'board',
        ])

    # ABSTRACT METHODS #######################################################
    def play(self, player: Player, play_dict: dict):
        return super().play(player=player, play_dict=play_dict)

    def is_playable_card(self, card: Card) -> bool:
        ...

    def winners(self) -> List[Player]:
        ...
