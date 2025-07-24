import logging
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes
)

from bot.decorators.logging import logging_basic_infos
from bot.functions.chat import (
    edit_message_text,
    send_alert,
    send_private_message,
    update_all_player_messages
)
from bot.functions.game import get_game
from bot.games.buttons.play_button import PlayButton
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.player import Player


@logging_basic_infos
async def close_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('CLOSE_GAME()')
    # user = update.effective_user
    message_id = update.effective_message.id
    query = update.callback_query
    data = query.data
    play_dict = PlayButton.callback_data_to_dict(data)
    game_id = play_dict[CallbackKeyEnum.GAME_ID]
    game = get_game(game_id=game_id, context=context)

    if game is None:
        text = 'Partida não encontrada.'
        return await edit_message_text(
            function_caller='CLOSE_GAME(GAME_NOT_FOUND)',
            new_text=text,
            context=context,
            message_id=message_id,
        )

    await send_alert(
        function_caller='CLOSE_GAME()',
        query=query,
        text='BOTÃO DE FECHAR AINDA NÃO FOI IMPLEMENTADO.'
    )


@logging_basic_infos
async def help_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('HELP_GAME()')
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    query = update.callback_query
    data = query.data
    play_dict = PlayButton.callback_data_to_dict(data)
    game_id = play_dict[CallbackKeyEnum.GAME_ID]
    game = get_game(game_id=game_id, context=context)

    if game is None:
        text = 'Partida não encontrada.'
        return await edit_message_text(
            function_caller='HELP_GAME(GAME_NOT_FOUND)',
            new_text=text,
            context=context,
            message_id=message_id,
        )

    text = game.DESCRIPTION
    if not isinstance(text, str):
        text = (
            f'DESCRIÇÃO DO JOGO "{game.DISPLAY_NAME}" NÃO FOI IMPLEMENTADA. '
            f'game.DESCRIPTION = ({game.DESCRIPTION})'
        )
    if callable(game.play_text_formatter):
        text = game.play_text_formatter(text)

    await send_private_message(
        function_caller='HELP_GAME()',
        context=context,
        text=text,
        user_id=user_id,
        markdown=False,
        # reply_markup=reply_markup,
    )


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
    # logging.info(f'{game}')
    play_response = game.play(player=player, play_dict=play_dict)

    if isinstance(play_response, str):
        await send_alert(
            function_caller='PLAY_GAME()',
            query=query,
            text=play_response
        )

    await update_all_player_messages(
        function_caller='PLAY_GAME()',
        game=game,
        context=context,
    )


# HANDLERS
PLAY_GAME_HANDLERS = [
    CallbackQueryHandler(
        close_game,
        pattern=PlayButton.callback_data_to_pattern(CommandEnum.CLOSE)
    ),
    CallbackQueryHandler(
        help_game,
        pattern=PlayButton.callback_data_to_pattern(CommandEnum.HELP)
    ),
    CallbackQueryHandler(
        play_game,
        pattern='|'.join((
            PlayButton.callback_data_to_pattern(CommandEnum.DRAW),
            PlayButton.callback_data_to_pattern(CommandEnum.PASS),
            PlayButton.callback_data_to_pattern(CommandEnum.PLAY),
            PlayButton.callback_data_to_pattern(CommandEnum.SELECT_COLOR),
        ))
    ),
]
