import logging
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes
)

from bot.decorators.logging import logging_basic_infos
from bot.functions.chat import edit_message_text, update_all_player_messages
from bot.functions.game import get_game
from bot.games.buttons.play_button import PlayButton
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.player import Player


@logging_basic_infos
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('PLAY_GAME()')
    user = update.effective_user
    message_id = update.effective_message.id
    query = update.callback_query
    data = query.data
    play_dict = PlayButton.callback_data_to_dict(data)
    game_id = play_dict[CallbackKeyEnum.GAME_ID]
    game = get_game(game_id=game_id, context=context)

    if game is None:
        text = 'Partida não encontrada.'
        return await edit_message_text(
            function_caller='PLAY_GAME(GAME_NOT_FOUND)',
            new_text=text,
            context=context,
            message_id=message_id,
        )

    player = Player(user=user)
    logging.info(f'Game: {game.DISPLAY_NAME} - game_id: {game_id}')
    logging.info(player)
    logging.info(f'Play Dict: {play_dict}')
    logging.info(f'{game}')
    game.play(player=player, play_dict=play_dict)

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
            PlayButton.callback_data_to_pattern(CommandEnum.SELECT_COLOR),
        ))
    )
]
