from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.decks.deck import BaseDeck
from bot.games.decks.nine_nine import NineNineDeck
from bot.games.player import Player


class NineNineBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = "💯99"
    DESCRIPTION: str = ""

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = NineNineDeck()
        super().__init__(
            draw_pile,
            *players,
            is_shuffle_deck=True,
            total_discard_pile=1,
            discard_at_start=True,
            initial_hand_size=4,
            hand_kwargs={"max_size": 4},
            min_total_players=2,
            max_total_players=10,
            debug=debug,
        )

        self.debug_attr_list.extend([])

    @property
    def discard_pile(self) -> BaseDeck:
        if self.discard_piles:
            return self.discard_piles[0]
        else:
            return None

    @property
    def total_score(self) -> int:
        result = 0
        discard_pile = self.discard_pile
        if discard_pile:
            for card in discard_pile:
                result += card.value
        return result
