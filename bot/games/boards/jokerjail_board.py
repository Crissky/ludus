from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.decks.royal import RoyalDeck
from bot.games.enums.card import FullRoyalNames, FullRoyalSuits
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
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

    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if self.is_started is not True:
            return self.invite_keyboard

        keyboard = PlayKeyBoard(buttons_per_row=3)
        if player != self.current_player:
            return keyboard
        if self.game_over:
            return keyboard

        for index, pile in enumerate(self.discard_piles):
            card = None
            if pile:
                card = pile.peek(quantity=1)[0]

            text = card.text if card else '❌'
            callback_data_args = {CallbackKeyEnum.HAND_POSITION.name: index}
            button = PlayButton(
                text=text,
                game=self,
                command=CommandEnum.PLAY,
                **callback_data_args

            )
            keyboard.add_button(button)

        if self.is_passing is True:
            button = self.pass_button
        else:
            button = self.draw_button
        keyboard.add_button(button)

        close_button = self.close_button
        help_button = self.help_button
        if isinstance(close_button, PlayButton):
            keyboard.add_button(close_button)
        if isinstance(help_button, PlayButton):
            keyboard.add_button(help_button)

        return keyboard
