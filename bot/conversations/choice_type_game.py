from random import choice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.callback import (
    LIST_DUEL_GAME_CALLBACK_DATA,
    LIST_PARTY_GAME_CALLBACK_DATA,
    LIST_SINGLE_GAME_CALLBACK_DATA
)
from bot.constants.choice_type_game import GREETINGS_TEXT
from bot.constants.handler_filters import (
    BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
    PREFIX_COMMANDS
)
from bot.functions.chat import send_private_message


async def choice_type_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    text = choice(GREETINGS_TEXT)
    text = text.format(user_name=user_name)
    text += f'👉 Qual tipo de jogo você quer jogar hoje, {user_name}?'
    keyboard_markup = get_choice_type_game_keyboard()

    await send_private_message(
        function_caller='CHOICE_TYPE_GAME()',
        context=context,
        text=text,
        user_id=user_id,
        reply_markup=keyboard_markup,
    )


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


CHOICE_TYPE_GAME_COMMANDS = ['start']
CHOICE_TYPE_GAME_HANDLERS = [
    PrefixHandler(
        prefix=PREFIX_COMMANDS,
        command=CHOICE_TYPE_GAME_COMMANDS,
        callback=choice_type_game,
        filters=BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
        has_args=False
    ),
    CommandHandler(
        command=CHOICE_TYPE_GAME_COMMANDS,
        callback=choice_type_game,
        filters=BASIC_COMMAND_IN_PRIVATE_CHAT_FILTER,
        has_args=False
    )
]
