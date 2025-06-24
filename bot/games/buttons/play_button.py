from bot.functions.buttons import (
    callback_data_to_dict,
    callback_data_to_string
)
from bot.games.boards.board import BaseBoard


from telegram import InlineKeyboardButton


class BasePlayButton:
    def __init__(self, game: BaseBoard, text: str, **callback_data):
        self.game = game
        self.text = text
        self.callback_data = callback_data

    def __eq__(self, value):
        if isinstance(value, BasePlayButton):
            return self.data_to_str == value.data_to_str
        return False

    @property
    def data_to_str(self) -> str:
        data = {
            'game_id': self.game.id,
            **self.callback_data
        }

        return callback_data_to_string(data)

    def str_to_data(self, data: str):
        return callback_data_to_dict(data)

    def make_button(self) -> InlineKeyboardButton:
        callback_data = self.data_to_str
        text = self.text
        return InlineKeyboardButton(text=text, callback_data=callback_data)
