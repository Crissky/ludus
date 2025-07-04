import logging
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes
)

from bot.decorators.logging import logging_basic_infos
from bot.functions.chat import update_all_player_messages
from bot.functions.game import get_game
from bot.games.buttons.play_button import PlayButton
from bot.games.enums.command import CommandEnum
from bot.games.player import Player


@logging_basic_infos
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('PLAY_GAME()')
    user = update.effective_user
    user_id = update.effective_user.id
    query = update.callback_query
    data = query.data
    data_dict = PlayButton.callback_data_to_dict(data)
    game_id = data_dict['game_id']
    game = get_game(game_id=game_id, context=context)
    player = Player(user=user)
    logging.info(f'Game: {game.DISPLAY_NAME} - game_id: {game_id}')
    logging.info(player)
    logging.info(f'Data Dict: {data_dict}')
    logging.info(f'{game}')
    game.next_turn()
    await update_all_player_messages(
        function_caller='PLAY_GAME()',
        game=game,
        context=context,
    )


# HANDLERS
PLAY_GAME_HANDLERS = [
    CallbackQueryHandler(
        play_game,
        pattern='|'.join((
            PlayButton.callback_data_to_pattern(CommandEnum.DRAW),
            PlayButton.callback_data_to_pattern(CommandEnum.PASS),
            PlayButton.callback_data_to_pattern(CommandEnum.PLAY),
        ))
    )
]
