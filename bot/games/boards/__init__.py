from bot.games.boards.board import BaseBoard
from bot.games.boards.colorgame_board import ColorGameBoard


def get_solo_board_list() -> list[BaseBoard]:
    solo_board_list = []

    return solo_board_list


def get_duel_board_list() -> list[BaseBoard]:
    duel_board_list = []

    return duel_board_list


def get_party_board_list() -> list[BaseBoard]:
    party_board_list = [
        ColorGameBoard,
    ]

    return party_board_list


def get_board_list() -> list[BaseBoard]:
    board_list = get_solo_board_list()
    board_list.extend(get_duel_board_list())
    board_list.extend(get_party_board_list())

    return sorted(board_list, key=lambda board: board.__name__)


def board_factory(board_name: str) -> BaseBoard:
    for board_class in get_board_list():
        if board_class.__name__ == board_name:
            return board_class
    raise ValueError(f'Board "{board_name}" não encontrada.')
