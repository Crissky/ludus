import logging
import re

from random import choice
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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
    MAIN_MENU_GAME_CALLBACK_DATA
)
from bot.constants.choice_type_game import GREETINGS_TEXT
from bot.constants.handler_filters import (
    BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
    PREFIX_COMMANDS
)
from bot.functions.chat import (
    edit_message_text,
    send_alert,
    send_private_message
)

from bot.functions.keyboard import reshape_row_buttons
from bot.functions.keyboard import get_back_button
from bot.functions.text import create_text_in_box
from bot.games.boards import get_party_board_list
from bot.games.boards.board import BaseBoard


# Conversation Functions
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
    keyboard_markup = create_board_list_keyboard(board_list)

    await edit_message_text(
        function_caller='LIST_PARTY_GAME()',
        new_text=text,
        context=context,
        message_id=message_id,
        reply_markup=keyboard_markup,
    )


# Buttons Functions
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
    ]

    return InlineKeyboardMarkup(buttons)


def create_board_list_keyboard(
    board_list: List[BaseBoard]
) -> InlineKeyboardMarkup:
    buttons = []
    for board in board_list:
        buttons.append(
            InlineKeyboardButton(
                text=board.DISPLAY_NAME,
                callback_data=board.__name__
            )
        )

    buttons = reshape_row_buttons(buttons=buttons, buttons_per_row=2)
    buttons.append([
        get_back_button(callback_data=MAIN_MENU_GAME_CALLBACK_DATA)
    ])

    return InlineKeyboardMarkup(buttons)


# Handlers
CHOICE_TYPE_GAME_COMMANDS = ['start']
CHOICE_TYPE_GAME_HANDLERS = [
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
    CallbackQueryHandler(
        choice_type_game,
        pattern=re.escape(MAIN_MENU_GAME_CALLBACK_DATA)
    ),
]
CHOICE_GAME_HANDLERS = [
    CallbackQueryHandler(
        list_single_game,
        pattern=re.escape(LIST_SINGLE_GAME_CALLBACK_DATA)
    ),
    CallbackQueryHandler(
        list_duel_game,
        pattern=re.escape(LIST_DUEL_GAME_CALLBACK_DATA)
    ),
    CallbackQueryHandler(
        list_party_game,
        pattern=re.escape(LIST_PARTY_GAME_CALLBACK_DATA)
    ),
]
