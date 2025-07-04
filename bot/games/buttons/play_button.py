
import re

from typing import TYPE_CHECKING, Union

from bot.games.enums.command import CommandEnum

from telegram import InlineKeyboardButton


if TYPE_CHECKING:
    from bot.games.boards.board import BaseBoard


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
        command: Union[CommandEnum, str],
        group: int = 0,
        **callback_data
    ):
        if isinstance(command, str):
            command = CommandEnum[command.upper()]
        if not isinstance(command, CommandEnum):
            raise TypeError(
                'Command precisa ser uma instância de CommandEnum '
                'ou uma striing válida de CommandEnum.'
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
        text = self.text
        callback_data = self.data_to_str

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

        callback_data: dict = eval(callback_data_str)
        callback_data = {
            PlayButton.CALLBACK_KEY_LIST[key]: value
            for key, value in callback_data.items()
        }

        return callback_data

    def str_to_data(self, data: str) -> dict:
        return self.callback_data_to_dict(data)

    @classmethod
    def callback_data_to_pattern(cls, command: Union[CommandEnum, str]) -> str:
        if isinstance(command, str):
            command = CommandEnum[command.upper()]
        if not isinstance(command, CommandEnum):
            raise TypeError(
                'Command precisa ser uma instância de CommandEnum '
                'ou uma striing válida de CommandEnum.'
            )

        data = {'command': command.name}

        return re.escape(cls.callback_data_to_string(data)[:-1])

    @property
    def data_to_str(self) -> str:
        data = {
            'command': self.command.name,
            'game_id': self.game.id,
        }
        data.update(self.callback_data)

        return PlayButton.callback_data_to_string(data)


if __name__ == '__main__':
    for command in CommandEnum:
        print(PlayButton.callback_data_to_pattern(command))
