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
from bot.functions.game import get_game, remove_game
from bot.games.buttons.play_button import PlayButton
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.player import Player


@logging_basic_infos
async def close_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('CLOSE_GAME()')
    user_name = update.effective_user.name
    message_id = update.effective_message.id
    query = update.callback_query
    data = query.data
    play_dict = PlayButton.callback_data_to_dict(data)
    game_id = play_dict[CallbackKeyEnum.GAME_ID]
    game = get_game(game_id=game_id, context=context)
    function_caller = 'CLOSE_GAME()'

    if game is None:
        text = 'Partida não encontrada.'
        return await edit_message_text(
            function_caller='CLOSE_GAME(GAME_NOT_FOUND)',
            new_text=text,
            context=context,
            message_id=message_id,
        )

    remove_game(game_id=game_id, context=context)

    await send_alert(
        function_caller=function_caller,
        query=query,
        text='Encerrando jogo...'
    )

    text = 'Jogo {game_name} ({game_id}) foi encerrado por {user_name}.'
    for player in game.player_list:
        logging.info(f'  Atualizando mensagem de {player} em {game.id}.')

        new_text = text.format(
            game_name=game.DISPLAY_NAME,
            game_id=game.id,
            user_name=user_name,
        )
        if callable(game.play_text_formatter):
            new_text = game.play_text_formatter(new_text)
        user_id = player.user_id
        message_id = player.message_id
        await edit_message_text(
            function_caller=function_caller,
            new_text=new_text,
            context=context,
            message_id=message_id,
            chat_id=user_id,
            user_id=user_id,
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
            PlayButton.callback_data_to_pattern(CommandEnum.CALCULATE),
        ))
    ),
]
