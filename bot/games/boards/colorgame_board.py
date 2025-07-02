from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.card import Card
from bot.games.decks.color import ColorDeck
from bot.games.player import Player


class ColorsGameBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = 'Colors'
    DESCRIPTION: str = None

    def __init__(self, *players: Player):
        draw_pile = ColorDeck()
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=1,
            initial_hand_size=7,
            hand_kwargs={},
            min_total_players=2,
            max_total_players=4,
        )
        self.pending_draw = 0

    def is_playable_card(self, card: Card) -> bool:
        if not self.discard_piles:
            return True

        top_card = self.discard_piles[0].peek()

        # Testa o empilhamento de carta PLUS
        if self.pending_draw > 0:
            if card.plus_value > 0 and card.plus_value >= top_card.plus_value:
                return True
            return False

        # Caso normal: tem que bater cor ou nome
        if (
            card.suit == top_card.suit or
            card.name == top_card.name or
            card.is_wild
        ):
            return True

        return False
