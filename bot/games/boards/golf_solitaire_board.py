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

    def create_board(self):
        for _ in range(self.num_rows):
            row = []
            for _ in range(self.num_card_per_row):
                card_list = self.draw()
                row.extend(card_list)
            self.board.extend(row)

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
                    CallbackKeyEnum.ROW_INDEX: row_index,
                    CallbackKeyEnum.CARD_INDEX: card_index,
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
    def draw_button(self):
        return PlayButton(
            text='🫴Comprar',
            game=self,
            command=CommandEnum.DRAW,
            group=1
        )
