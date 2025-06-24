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
        self.play_buttons: List[BasePlayButton] = []

        for play_button in play_buttons:
            self.add_button(play_button)

    def add_button(self, button: BasePlayButton):
        if button in self.play_buttons:
            raise ValueError('Já existe um botão com esse nome.')
        if not isinstance(button, BasePlayButton):
            raise ValueError(
                'O botão deve ser uma instância de BasePlayButton.'
            )
        self.play_buttons.append(button)

    @property
    def buttons(self) -> List[List[InlineKeyboardButton]]:
        button_lists = []
        for i in range(0, len(self.play_buttons), self.buttons_per_row):
            row = self.play_buttons[i:i+self.buttons_per_row]
            button_lists.append([button.make_button() for button in row])

        return button_lists

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        button_lists = self.buttons

        return InlineKeyboardMarkup(button_lists)
