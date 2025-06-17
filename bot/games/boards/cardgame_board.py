from typing import List
from bot.games.boards.board import BaseBoard
from bot.games.decks.deck import BaseDeck
from bot.games.hands.hand import BaseHand
from bot.games.player import Player


class CardGameBoard(BaseBoard):
    def __init__(
        self,
        name: str,
        player_list: List[Player],
        draw_pile: BaseDeck,
        total_discard_pile: int = 1,
        initial_hand_size: int = 7,
        hand_kwargs: dict = None
    ):
        super().__init__(name, player_list)
        if hand_kwargs is None:
            hand_kwargs = {}
        self.create_draw_pile(draw_pile)
        self.create_discard_pile(total_discard_pile)
        self.create_hands(player_list, hand_kwargs)

        self.distribute_cards(player_list, initial_hand_size)

    def create_draw_pile(self, draw_pile: BaseDeck):
        self.draw_pile = draw_pile
        self.draw_pile.shuffle()

    def create_discard_pile(self, total_discard_pile: int):
        self.discard_piles = [BaseDeck() for _ in range(total_discard_pile)]

    def create_hands(self, player_list: List[Player], hand_kwargs: dict):
        self.player_hands = {
            player: BaseHand(**hand_kwargs)
            for player in player_list
        }

    def distribute_cards(self, player_list, initial_hand_size):
        for i in range(initial_hand_size):
            for player in player_list:
                self.player_hands[player].add_card(self.draw_pile.draw())
