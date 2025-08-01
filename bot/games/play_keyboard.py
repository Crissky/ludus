from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.games.buttons.play_button import PlayButton


class PlayKeyBoard:
    def __init__(
        self,
        buttons_per_row: int = 1,
        *play_buttons: PlayButton
    ):
        if buttons_per_row < 1:
            raise ValueError(
                'O número de botões por linha deve ser maior que 0.'
            )

        self.buttons_per_row = buttons_per_row
        self.play_button_list: List[PlayButton] = []

        for play_button in play_buttons:
            self.add_button(play_button)

    def __str__(self) -> str:
        return '\n'.join(
            str(button) for button in self.play_button_list
        )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'buttons_per_row={self.buttons_per_row},'
            f'play_button_list={self.play_button_list}'
            ')'
        )

    def add_button(self, button: PlayButton):
        if button in self.play_button_list:
            raise ValueError('Esse botão já está no teclado.')
        if not isinstance(button, PlayButton):
            raise ValueError(
                f'O botão deve ser uma instância de {PlayButton.__name__}.'
            )
        self.play_button_list.append(button)

    def make_buttons(self) -> List[List[InlineKeyboardButton]]:
        button_lists = []
        sorted_play_button_list = sorted(
            self.play_button_list,
            key=lambda x: x.group
        )

        i = 0
        group = 0
        for play_button in sorted_play_button_list:
            if i % self.buttons_per_row == 0 or play_button.group > group:
                i = 0
                group = play_button.group
                row = []
                button_lists.append(row)

            row.append(play_button.make_button())
            i += 1

        return button_lists

    def make_keyboard(self) -> InlineKeyboardMarkup:
        button_lists = self.make_buttons()

        return InlineKeyboardMarkup(button_lists)


class InviteKeyBoard(PlayKeyBoard):
    def __init__(self, keyboard: InlineKeyboardMarkup):
        self.keyboard = keyboard

    def __str__(self) -> str:
        return f'{self.keyboard}'

    def make_keyboard(self) -> InlineKeyboardMarkup:
        return self.keyboard
