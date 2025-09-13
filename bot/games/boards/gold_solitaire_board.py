from typing import List

from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.card import Card
from bot.games.player import Player


class GolfSolitaireBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = '🏌️‍♂️Gold Solitaire'
    DESCRIPTION: str = ('')

    # ABSTRACT METHODS #######################################################
    def play(self, player: Player, play_dict: dict):
        return super().play(player=player, play_dict=play_dict)

    def is_playable_card(self, card: Card) -> bool:
        ...

    def winners(self) -> List[Player]:
        ...
