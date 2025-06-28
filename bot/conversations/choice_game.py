import logging

from random import choice
from typing import List
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
    SELECT_GAME_CALLBACK_DATA
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
    send_private_message
)

from bot.functions.game import add_game, get_game
from bot.functions.keyboard import reshape_row_buttons
from bot.functions.keyboard import get_back_button
from bot.functions.text import create_text_in_box
from bot.games.boards import board_factory, get_party_board_list
from bot.games.boards.board import BaseBoard
from bot.games.player import Player


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


async def list_single_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('LIST_SINGLE_GAME()')
    query = update.callback_query
    text = 'Desculpe, mas ainda não temos jogos da categoria "🎯 Solo".'

    await send_alert(
        function_caller='LIST_SINGLE_GAME()',
        query=query,
        text=text,
    )


async def list_duel_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('LIST_DUEL_GAME()')
    query = update.callback_query
    text = 'Desculpe, mas ainda não temos jogos da categoria "⚔️ Duelo".'

    await send_alert(
        function_caller='LIST_DUEL_GAME()',
        query=query,
        text=text,
    )


async def list_party_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('LIST_PARTY_GAME()')
    message_id = update.effective_message.id
    user_name = update.effective_user.name
    text = f'👉 Qual jogo de Grupo você quer jogar, {user_name}?'
    text = create_text_in_box(
        text=text,
        footer_text='Escolha o jogo',
        footer_emoji1='👇',
        footer_emoji2='👇',
        clean_func=None,
    )

    board_list = get_party_board_list()
    keyboard_markup = get_board_list_keyboard(board_list)

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
    player = Player(user=user)
    game = game_class(player)
    game_id = game.id
    text = game.show_board()
    text = create_text_in_box(
        text=text,
        header_text=game.DISPLAY_NAME,
        footer_text='Enviar convite',
        footer_emoji1='👇',
        footer_emoji2='👇',
        clean_func=None,
    )
    reply_markup = get_invite_keyboard(game_id)

    add_game(game=game, context=context)

    await edit_message_text(
        function_caller='SELECT_GAME()',
        new_text=text,
        context=context,
        message_id=message_id,
        reply_markup=reply_markup,
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
        game.add_player(player=player)
        text = game.show_board()
        text = create_text_in_box(
            text=text,
            header_text=game.DISPLAY_NAME,
            footer_text='Convite',
            footer_emoji1='🔗',
            footer_emoji2='🔗',
            clean_func=None,
        )
        reply_markup = get_invite_keyboard(game_id=game_id)

        await send_private_message(
            function_caller='INVITE_GAME()',
            context=context,
            text=text,
            user_id=user_id,
            reply_markup=reply_markup,
        )
    else:
        text = str(args)
        await send_private_message(
            function_caller='INVITE_GAME()',
            context=context,
            text=text,
            user_id=user_id,
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
        [InlineKeyboardButton("Entrar na Partida", url=invite_link)],
        [InlineKeyboardButton("Copiar Convite", copy_text=copy_button)],
        [get_close_button()]
    ])

    return reply_markup


def get_invite_link(game_id: int):
    bot_username = 'LudusCardBot'
    return f"https://t.me/{bot_username}?start=invite_{game_id}"


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
        list_single_game,
        pattern=LIST_SINGLE_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        list_duel_game,
        pattern=LIST_DUEL_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        list_party_game,
        pattern=LIST_PARTY_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        select_game,
        pattern=SELECT_GAME_CALLBACK_DATA
    ),
]
