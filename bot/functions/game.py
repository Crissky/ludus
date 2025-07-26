from typing import Union
from telegram.ext import ContextTypes

from bot.games.boards.board import BaseBoard


def add_game(game: BaseBoard, context: ContextTypes.DEFAULT_TYPE):
    game_id = game.id
    game_dict = context.bot_data.get('games', {})
    game_dict[game_id] = game

    if 'games' not in context.bot_data:
        context.bot_data['games'] = game_dict


def get_game(
    game_id: Union[int, str],
    context: ContextTypes.DEFAULT_TYPE
) -> BaseBoard:
    if isinstance(game_id, str):
        game_id = int(game_id)

    game_dict = context.bot_data.get('games', {})

    return game_dict.get(game_id)


def remove_game(game_id: Union[int, str], context: ContextTypes.DEFAULT_TYPE):
    if isinstance(game_id, str):
        game_id = int(game_id)

    game_dict = context.bot_data.get('games', {})
    game_dict.pop(game_id, None)
