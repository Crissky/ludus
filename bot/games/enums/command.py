from enum import Enum


class CallbackKeyEnum(Enum):
    COMMAND = 'command'
    GAME_ID = 'game_id'
    HAND_POSITION = 'hand_position'
    SELECTED_COLOR = 'selected_color'


class CommandEnum(Enum):
    DRAW = 'draw'
    PASS = 'pass'
    PLAY = 'play'
