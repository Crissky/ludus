
import re

from typing import TYPE_CHECKING, Union

from bot.games.enums.command import CallbackKeyEnum, CommandEnum

from telegram import InlineKeyboardButton


if TYPE_CHECKING:
    from bot.games.boards.board import BaseBoard


class PlayButton:
    CALLBACK_KEY_LIST = [enum for enum in CallbackKeyEnum]

    def __init__(
        self,
        text: str,
        game: 'BaseBoard',
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

        self.text = text
        self.game = game
        self.command = command
        self.group = group
        self.callback_data = callback_data
        self.check_callback_data()

    def __eq__(self, value):
        if isinstance(value, PlayButton):
            return self.data_to_str == value.data_to_str

        return False

    def __str__(self) -> str:
        return f'{self.text}'

    def __repr__(self) -> str:
        text = ','.join(f'{k}={v}' for k, v in self.callback_data.items())
        return (
            f'{self.__class__.__name__}('
            f'text={self.text},'
            f'command={self.command},'
            f'group={self.group}'
            f'{text}'
            ')'
        )

    def check_callback_data(self):
        error_list = [
            key
            for key in self.callback_data.keys()
            if key not in CallbackKeyEnum._member_names_
        ]

        if error_list:
            raise ValueError(
                f'callback_data inválido(s): {error_list}.'
                f'\nOs valores válidos são: {CallbackKeyEnum._member_names_}.'
            )

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

        data = {CallbackKeyEnum.COMMAND: command.name}

        return re.escape(cls.callback_data_to_string(data)[:-1])

    @property
    def data_to_str(self) -> str:
        data = {
            CallbackKeyEnum.COMMAND: self.command.name,
            CallbackKeyEnum.GAME_ID: self.game.id,
        }
        callback_data_dict = {
            CallbackKeyEnum[key]: value
            for key, value in self.callback_data.items()
        }
        data.update(callback_data_dict)

        return PlayButton.callback_data_to_string(data)


if __name__ == '__main__':
    for command in CommandEnum:
        print(PlayButton.callback_data_to_pattern(command))
