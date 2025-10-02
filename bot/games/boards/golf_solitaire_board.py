from typing import List

from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.decks.royal import RoyalDeck
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
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

    def get_card(self, row_index: int, card_index: int) -> Card:
        if row_index < 0 or row_index >= self.num_rows:
            return None
        if card_index < 0 or card_index >= self.num_card_per_row:
            return None

        row = self.board[row_index]
        card = row[card_index]

        return card

    def is_match_card(self, card1: Card, card2: Card) -> bool:
        result = False
        value1 = card1.value
        value2 = card2.value
        max_value = len(card1.name.__class__) - 1

        if value1 == 0 and value2 == max_value:
            result = True
        elif value2 == 0 and value1 == max_value:
            result = True
        elif abs(value1 - value2) == 1:
            result = True

        return result

    def count_neighbors(self, row_index: int, card_index: int) -> int:
        neighbors = [
            self.get_card(row_index + 1, card_index),
            self.get_card(row_index - 1, card_index),
            self.get_card(row_index, card_index + 1),
            self.get_card(row_index, card_index - 1),
        ]

        return sum((1 for neighbor in neighbors if isinstance(neighbor, Card)))

    def is_valid_play(self, row_index: int, card_index: int) -> bool:
        result = False
        card = self.get_card(row_index, card_index)
        top_card = self.top_discard_card
        is_match = self.is_match_card(card, top_card)
        total_board = self.total_board_cards

        total_neighbors = []
        for r_i, c_i in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            neighbor_card = self.get_card(row_index=r_i, card_index=c_i)
            if isinstance(neighbor_card, Card):
                total = self.count_neighbors(row_index=r_i, card_index=c_i)
                total_neighbors.append(total)

        if card is None:
            result = False
        elif total_board <= 2:
            result = True
        elif is_match is True and 1 not in total_neighbors:
            result = True

        return result

    def create_board(self):
        for _ in range(self.num_rows):
            row = []
            for _ in range(self.num_card_per_row):
                card_list = self.draw()
                row.extend(card_list)
            self.board.append(row)

    # ABSTRACT METHODS #######################################################
    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if self.is_started is not True:
            return self.invite_keyboard

        keyboard = PlayKeyBoard(buttons_per_row=self.num_card_per_row)
        if self.game_over:
            return keyboard

        for row_index, row in enumerate(self.board):
            for card_index, card in enumerate(row):
                text = text = card.text if card else '❌'
                callback_data_args = {
                    CallbackKeyEnum.ROW_INDEX.name: row_index,
                    CallbackKeyEnum.CARD_INDEX.name: card_index,
                }
                button = PlayButton(
                    text=text,
                    game=self,
                    command=CommandEnum.PLAY,
                    group=row_index,
                    **callback_data_args
                )
                keyboard.add_button(button)

        if self.draw_pile.is_empty is False:
            keyboard.add_button(self.draw_button)

        return keyboard

    def play(self, player: Player, play_dict: dict):
        result = super().play(player=player, play_dict=play_dict)
        if isinstance(result, str):
            return result

        command_str = play_dict[CallbackKeyEnum.COMMAND]
        command_enum = CommandEnum[command_str]
        row_index = play_dict.get(CallbackKeyEnum.ROW_INDEX)
        card_index = play_dict.get(CallbackKeyEnum.CARD_INDEX)

    def is_playable_card(self, card: Card) -> bool:
        return True

    def winners(self) -> List[Player]:
        winners = []
        if self.is_started is True and self.board:
            total_cards = sum((len(row) for row in self.board))
            if total_cards == 0:
                winners.append(self.player)
        elif not winners and self.draw_pile.is_empty:
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
    def top_discard_card(self) -> Card:
        if self.discard_pile:
            card_list = self.discard_pile.peek(quantity=1)
            return card_list[0] if card_list else None
        else:
            return None

    @property
    def total_board_cards(self) -> int:
        count = 0
        for row in self.board:
            for card in row:
                if isinstance(card, Card):
                    count += 1

        return count
