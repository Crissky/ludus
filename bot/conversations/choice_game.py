from functools import partial
import logging

from random import choice
from typing import List
from decouple import config
from telegram import (
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler
)

from bot.constants.callback import (
    LIST_DUEL_GAME_CALLBACK_DATA,
    LIST_PARTY_GAME_CALLBACK_DATA,
    LIST_SINGLE_GAME_CALLBACK_DATA,
    MAIN_MENU_GAME_CALLBACK_DATA,
    SELECT_GAME_CALLBACK_DATA,
    START_GAME_CALLBACK_DATA
)
from bot.constants.choice_type_game import GREETINGS_TEXT
from bot.constants.handler_filters import (
    BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators.logging import logging_basic_infos
from bot.functions.buttons import get_close_button
from bot.functions.chat import (
    edit_message_text,
    send_alert,
    send_private_message,
    update_all_player_messages
)

from bot.functions.game import add_game, get_game
from bot.functions.keyboard import reshape_row_buttons
from bot.functions.keyboard import get_back_button
from bot.functions.text import create_text_in_box
from bot.games.boards import board_factory, get_party_board_list
from bot.games.boards.board import BaseBoard
from bot.games.player import Player


BOT_USERNAME = config("BOT_USERNAME")


# CONVERSATION FUNCTIONS
@logging_basic_infos
async def choice_type_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('CHOICE_TYPE_GAME()')
    user_id = update.effective_user.id
    user_name = update.effective_user.name

    if (query := update.callback_query):
        text = ''
    else:
        text = choice(GREETINGS_TEXT)
        text = text.format(user_name=user_name)
        text += '\n\n'

    text += f'👉 Qual tipo de jogo você quer jogar hoje, {user_name}?'
    text = create_text_in_box(
        text=text,
        footer_text='Escolha o tipo de jogo',
        footer_emoji1='👇',
        footer_emoji2='👇',
        clean_func=None,
    )
    keyboard_markup = get_choice_type_game_keyboard()

    if query:
        message_id = query.message.message_id
        await edit_message_text(
            function_caller='LIST_PARTY_GAME()',
            new_text=text,
            context=context,
            message_id=message_id,
            reply_markup=keyboard_markup,
        )
    else:
        await send_private_message(
            function_caller='CHOICE_TYPE_GAME()',
            context=context,
            text=text,
            user_id=user_id,
            reply_markup=keyboard_markup,
        )


async def list_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('LIST_GAMES()')
    message_id = update.effective_message.id
    user_name = update.effective_user.name
    query = update.callback_query
    data = query.data

    text = f'👉 Qual jogo de Grupo você quer jogar, {user_name}?'
    board_list = None
    keyboard_markup = None
    if data == LIST_SINGLE_GAME_CALLBACK_DATA:
        text = 'Desculpe, mas ainda não temos jogos da categoria "🎯 Solo".'
    elif data == LIST_DUEL_GAME_CALLBACK_DATA:
        text = 'Desculpe, mas ainda não temos jogos da categoria "⚔️ Duelo".'
    elif data == LIST_PARTY_GAME_CALLBACK_DATA:
        board_list = get_party_board_list()
        keyboard_markup = get_board_list_keyboard(board_list)
    else:
        text = f'Lista de jogos "{data}" não foi encontrada!!!'

    if board_list is None or keyboard_markup is None:
        await send_alert(
            function_caller='LIST_GAMES()',
            query=query,
            text=text,
        )
        return

    text = create_text_in_box(
        text=text,
        footer_text='Escolha o jogo',
        footer_emoji1='👇',
        footer_emoji2='👇',
        clean_func=None,
    )

    await edit_message_text(
        function_caller='LIST_PARTY_GAME()',
        new_text=text,
        context=context,
        message_id=message_id,
        reply_markup=keyboard_markup,
    )


async def select_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('SELECT_GAME()')
    user = update.effective_user
    message_id = update.effective_message.id
    query = update.callback_query
    data = query.data

    game_name = data.replace(SELECT_GAME_CALLBACK_DATA, '')
    game_class = board_factory(game_name)
    player = Player(user=user, message_id=message_id)
    game = game_class(player)
    game_id = game.id
    invite_keyboard = get_invite_keyboard(game_id)
    invite_text_formatter = partial(
        create_text_in_box,
        header_text=game.DISPLAY_NAME,
        footer_text='Enviar convite',
        footer_emoji1='👇',
        footer_emoji2='👇',
        clean_func=None,
    )
    play_text_formatter = partial(
        create_text_in_box,
        header_text=game.DISPLAY_NAME,
        clean_func=None,
    )
    game.set_invite_keyboard(keyboard=invite_keyboard)
    game.set_invite_text_formatter(formatter=invite_text_formatter)
    game.set_play_text_formatter(formatter=play_text_formatter)
    add_game(game=game, context=context)

    await update_all_player_messages(
        function_caller='SELECT_GAME()',
        game=game,
        context=context,
    )


@logging_basic_infos
async def invite_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('INVITE_GAME()')
    user = update.effective_user
    user_id = update.effective_user.id
    args = context.args
    arg_text = args[0]

    if arg_text.startswith('invite_'):
        game_id = arg_text.replace('invite_', '')
        game = get_game(game_id=game_id, context=context)
        if game is None:
            text = 'Partida não encontrada.'
            return await send_private_message(
                function_caller='INVITE_GAME(GAME_NOT_FOUND)',
                context=context,
                text=text,
                user_id=user_id,
            )

        player = Player(user=user)
        if game.is_started and not game.player_in_game(player=player):
            text = 'Não é possível entrar nessa partida, pois já foi iniciada.'
            return await send_private_message(
                function_caller='INVITE_GAME(GAME_STARTED)',
                context=context,
                text=text,
                user_id=user_id,
            )

        game.add_player(player=player)

        await update_all_player_messages(
            function_caller='INVITE_GAME()',
            game=game,
            context=context,
        )
    else:
        text = str(args)
        await send_private_message(
            function_caller='INVITE_GAME()',
            context=context,
            text=text,
            user_id=user_id,
        )


@logging_basic_infos
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('START_GAME()')
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    query = update.callback_query
    data = query.data
    game_id = data.replace(START_GAME_CALLBACK_DATA, '')
    game = get_game(game_id=game_id, context=context)
    if game is None:
        text = 'Partida não encontrada.'
        return await edit_message_text(
            function_caller='START_GAME(GAME_NOT_FOUND)',
            new_text=text,
            context=context,
            message_id=message_id,
        )

    host_player = game.host
    if host_player is not None and host_player == user_id:
        game.start()
        await update_all_player_messages(
            function_caller='START_GAME()',
            game=game,
            context=context,
        )
    else:
        await send_alert(
            function_caller='START_GAME()',
            query=query,
            text='Apenas o host pode iniciar a partida.',
        )


# BUTTONS FUNCTIONS
def get_choice_type_game_keyboard() -> InlineKeyboardMarkup:
    single_text = '🎯 Solo'
    duel_text = '⚔️ Duelo'
    party_text = '🎉 Grupo'
    buttons = [
        [
            InlineKeyboardButton(
                text=single_text,
                callback_data=LIST_SINGLE_GAME_CALLBACK_DATA
            )
        ],
        [
            InlineKeyboardButton(
                text=duel_text,
                callback_data=LIST_DUEL_GAME_CALLBACK_DATA
            )
        ],
        [
            InlineKeyboardButton(
                text=party_text,
                callback_data=LIST_PARTY_GAME_CALLBACK_DATA
            )
        ],
        [
            get_close_button()
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def get_board_list_keyboard(
    board_list: List[BaseBoard]
) -> InlineKeyboardMarkup:
    buttons = []
    for board in board_list:
        buttons.append(
            InlineKeyboardButton(
                text=board.DISPLAY_NAME,
                callback_data=f'{SELECT_GAME_CALLBACK_DATA}{board.__name__}'
            )
        )

    buttons = reshape_row_buttons(buttons=buttons, buttons_per_row=2)
    buttons.append([
        get_back_button(callback_data=MAIN_MENU_GAME_CALLBACK_DATA),
        get_close_button(right_icon=True)
    ])

    return InlineKeyboardMarkup(buttons)


def get_invite_keyboard(game_id: int) -> InlineKeyboardMarkup:
    invite_link = get_invite_link(game_id)
    copy_button = CopyTextButton(text=invite_link)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🚀Iniciar Partida",
            callback_data=f'{START_GAME_CALLBACK_DATA}{game_id}'
        )],
        [InlineKeyboardButton(
            "📨Enviar Convite",
            switch_inline_query=invite_link
        )],
        [InlineKeyboardButton("📩Copiar Convite", copy_text=copy_button)],
        [get_close_button()]
    ])

    return reply_markup


def get_invite_link(game_id: int):
    return f"https://t.me/{BOT_USERNAME}?start=invite_{game_id}"


# HANDLERS
CHOICE_TYPE_GAME_COMMANDS = ['start']
CHOICE_GAME_HANDLERS = [
    PrefixHandler(
        prefix=PREFIX_COMMANDS,
        command=CHOICE_TYPE_GAME_COMMANDS,
        callback=choice_type_game,
        filters=BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
    ),
    CommandHandler(
        command=CHOICE_TYPE_GAME_COMMANDS,
        callback=choice_type_game,
        filters=BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
        has_args=False
    ),
    CommandHandler(
        command=CHOICE_TYPE_GAME_COMMANDS,
        callback=invite_game,
        filters=BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
        has_args=True
    ),
    CallbackQueryHandler(
        choice_type_game,
        pattern=MAIN_MENU_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        list_games,
        pattern=(
            f'{LIST_SINGLE_GAME_CALLBACK_DATA}'
            f'|{LIST_DUEL_GAME_CALLBACK_DATA}'
            f'|{LIST_PARTY_GAME_CALLBACK_DATA}'
        )
    ),
    CallbackQueryHandler(
        select_game,
        pattern=SELECT_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        start_game,
        pattern=START_GAME_CALLBACK_DATA
    ),
]
