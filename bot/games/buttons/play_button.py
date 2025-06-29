
from typing import TYPE_CHECKING

from bot.games.enums.command import CommandEnum

from telegram import InlineKeyboardButton

if TYPE_CHECKING:
    from bot.games.boards.board import BaseBoard


from telegram import InlineKeyboardButton


class PlayButton:
    CALLBACK_KEY_LIST = [
        'command',
        'game_id',
        'hand_position',
    ]

    def __init__(
        self,
        game: 'BaseBoard',
        text: str,
        command: str,
        group: int = 0,
        **callback_data
    ):
        if not isinstance(command, CommandEnum):
            raise TypeError(
                'Command precisa ser uma instância de CommandEnum.'
            )

        self.game = game
        self.text = text
        self.command = command
        self.group = group
        self.callback_data = callback_data

    def __eq__(self, value):
        if isinstance(value, PlayButton):
            return self.data_to_str == value.data_to_str
        return False

    def make_button(self) -> InlineKeyboardButton:
        callback_data = self.data_to_str
        text = self.text
        return InlineKeyboardButton(text=text, callback_data=callback_data)

    # CALLBACK FUNCTIONS
    @classmethod
    def callback_data_to_string(cls, callback_data: dict) -> str:
        '''Transforma um dicionário em uma string compactada usada no
        campo data de um botão.
        '''

        items = []
        for key, value in callback_data.items():
            key_int = PlayButton.CALLBACK_KEY_LIST.index(key)
            if isinstance(value, str):
                items.append(f'{key_int}:"{value}"')
            else:
                items.append(f'{key_int}:{value}')
        text = ','.join(items)
        text = f'{{{text}}}'

        return text

    @classmethod
    def callback_data_to_dict(cls, callback_data_str: str) -> dict:
        '''Transforma de volta uma string compactada usada no campo data
        de um botão em um dicionário.
        '''

        callback_data = eval(callback_data_str)
        callback_data = {
            PlayButton.CALLBACK_KEY_LIST[key]: value
            for key, value in callback_data.items()
        }
        return callback_data

    def str_to_data(self, data: str) -> dict:
        return self.callback_data_to_dict(data)

    @property
    def data_to_str(self) -> str:
        data = {
            'command': self.command.name,
            'game_id': self.game.id,
        }
        data.update(self.callback_data)

        return PlayButton.callback_data_to_string(data)
