import logging

from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.decks.warfare import TerritoriesDeck
from bot.games.player import Player

logger = logging.getLogger(__name__)


class WarfareBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = "🌎Warfare"
    DESCRIPTION: str = "DESCRIÇÃO E REGRAS DO WARFARE PRECISAM SER DEFINIDAS."

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = TerritoriesDeck()
        super().__init__(
            draw_pile,
            *players,
            is_shuffle_deck=True,
            total_discard_pile=1,
            discard_at_start=True,
            initial_hand_size=0,
            hand_kwargs={},
            min_total_players=3,
            max_total_players=6,
            debug=debug,
        )
