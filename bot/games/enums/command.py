from enum import Enum


class CallbackKeyEnum(Enum):
    COMMAND = 'command'
    GAME_ID = 'game_id'
    HAND_POSITION = 'hand_position'
    DISCARD_POSITION = 'discard_position'
    SELECTED_COLOR = 'selected_color'


class CommandEnum(Enum):
    CLOSE = 'close'
    DRAW = 'draw'
    HELP = 'help'
    PASS = 'pass'
    PLAY = 'play'
    SELECT_COLOR = 'select color'
