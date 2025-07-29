from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
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

    def create_discard_pile(self):
        self.discard_piles = [
            BaseDeck()
            for _ in range(self.total_discard_pile)
        ]

        for _ in range(6):
            for index in self.wall_indexes:
                wall_pile = self.discard_piles[index]
                cards = self.draw()
                wall_pile.add(*cards)

        for _ in range(2):
            for index in self.corner_indexes:
                corner_pile = self.discard_piles[index]
                cards = self.draw()
                corner_pile.add(*cards)

        joker_pile = self.discard_piles[self.joker_indexes[0]]
        joker_pile.add(self.joker_card)
