from typing import List, Type
from bot.games.boards.board import BaseBoard
from bot.games.boards.colorgame_board import ColorsGameBoard
from bot.games.boards.golf_solitaire_board import GolfSolitaireBoard
from bot.games.boards.jokerjail_board import JokerJailBoard
from bot.games.boards.nine_nine_board import NineNineBoard
from bot.games.boards.scoundrel_board import ScoundrelBoard


def get_solo_board_list() -> List[Type[BaseBoard]]:
    solo_board_list = [
        ScoundrelBoard,
        JokerJailBoard,
        GolfSolitaireBoard,
    ]

    return solo_board_list


def get_duel_board_list() -> List[Type[BaseBoard]]:
    duel_board_list = []

    return duel_board_list


def get_party_board_list() -> List[Type[BaseBoard]]:
    party_board_list = [
        ColorsGameBoard,
        NineNineBoard,
    ]

    return party_board_list


def get_board_list() -> List[Type[BaseBoard]]:
    board_list = []
    board_list.extend(get_solo_board_list())
    board_list.extend(get_duel_board_list())
    board_list.extend(get_party_board_list())

    return sorted(board_list, key=lambda board: board.__name__)


def board_factory(board_name: str) -> Type[BaseBoard]:
    for board_class in get_board_list():
        if board_class.__name__ == board_name:
            return board_class
    raise ValueError(f'Board "{board_name}" não encontrada.')
