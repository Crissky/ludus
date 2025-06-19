from typing import List
from telegram import InlineKeyboardButton

from bot.games.buttons.play_button import BasePlayButton


class PlayKeyBoard:
    def __init__(self, buttons_per_row: int = 1, *play_buttons: BasePlayButton):
        self.buttons_per_row = buttons_per_row
        self.play_buttons = list(play_buttons)

    def get_keyboard(self) -> List[List[InlineKeyboardButton]]:
        keyboard = []
        for i in range(0, len(self.play_buttons), self.buttons_per_row):
            row = self.play_buttons[i:i+self.buttons_per_row]
            keyboard.append([button.make_button() for button in row])

        return keyboard

    def add_button(self, button: BasePlayButton):
        self.play_buttons.append(button)
