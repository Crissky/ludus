from bot.games.boards.board import BaseBoard
from bot.games.boards.colorgame_board import ColorGameBoard


BOARD_LIST = [
    ColorGameBoard,
]


def board_factory(board_name: str) -> BaseBoard:
    for board_class in BOARD_LIST:
        if board_class.__name__ == board_name:
            return board_class
    raise ValueError(f'Board "{board_name}" não encontrada.')
