from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.games.buttons.play_button import BasePlayButton


class PlayKeyBoard:
    def __init__(
        self,
        buttons_per_row: int = 1,
        *play_buttons: BasePlayButton
    ):
        if buttons_per_row < 1:
            raise ValueError(
                'O número de botões por linha deve ser maior que 0.'
            )

        self.buttons_per_row = buttons_per_row
        self.play_button_list: List[BasePlayButton] = []

        for play_button in play_buttons:
            self.add_button(play_button)

    def add_button(self, button: BasePlayButton):
        if button in self.play_button_list:
            raise ValueError('Já existe um botão com esse nome.')
        if not isinstance(button, BasePlayButton):
            raise ValueError(
                'O botão deve ser uma instância de BasePlayButton.'
            )
        self.play_button_list.append(button)

    @property
    def buttons(self) -> List[List[InlineKeyboardButton]]:
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

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        button_lists = self.buttons

        return InlineKeyboardMarkup(button_lists)
