from typing import List

from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.decks.royal import RoyalDeck
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
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
        self.num_rows = 5
        self.num_card_per_row = 7
        self.board: List[Card] = []
        self.create_board()

        self.debug_attr_list.extend([
            'board',
        ])

    def create_board(self):
        for _ in range(self.num_rows):
            row = []
            for _ in range(self.num_card_per_row):
                card_list = self.draw()
                row.extend(card_list)
            self.board.extend(row)

    # ABSTRACT METHODS #######################################################
    def play(self, player: Player, play_dict: dict):
        return super().play(player=player, play_dict=play_dict)

    def is_playable_card(self, card: Card) -> bool:
        return True

    def winners(self) -> List[Player]:
        winners = []
        if self.board:
            total_cards = sum((len(row) for row in self.board))
            if total_cards == 0:
                winners.append(self.player)

        if not winners and self.draw_pile.is_empty:
            winners.append(self.enemy)

        return winners

    @property
    def player(self) -> Player:
        return self.player_list[0] if self.player_list else None

    @property
    def discard_pile(self) -> BaseDeck:
        if self.discard_piles:
            return self.discard_piles[0]
        else:
            return None

    @property
    def draw_button(self):
        return PlayButton(
            text='🫴Comprar',
            game=self,
            command=CommandEnum.DRAW,
            group=1
        )
