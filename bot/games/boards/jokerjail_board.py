from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.card import Card
from bot.games.decks.royal import RoyalDeck
from bot.games.enums.card import FullRoyalNames, FullRoyalSuits
from bot.games.player import Player


class JokerJailBoard(BaseCardGameBoard):
    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = RoyalDeck(is_shuffle=True)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=9,
            discard_at_start=True,
            initial_hand_size=0,
            hand_kwargs={'max_size': 0},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.joker_card = Card(
            name=FullRoyalNames.JOKER,
            suit=FullRoyalSuits.JOKER
        )
        self.wall_indexes = [1, 3, 5, 7]
        self.corner_indexes = [0, 2, 6, 8]
        self.joker_indexes = [4]

        self.debug_attr_list.extend([
            'joker_card',
            'wall_indexes',
            'corner_indexes',
            'joker_indexes',
        ])

    # TODO
    def create_discard_pile(self):
        ...
