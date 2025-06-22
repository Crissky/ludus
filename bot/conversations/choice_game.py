from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from bot.constants.callback import (
    LIST_DUEL_GAME_CALLBACK_DATA,
    LIST_PARTY_GAME_CALLBACK_DATA,
    LIST_SINGLE_GAME_CALLBACK_DATA
)


async def list_single_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...


async def list_duel_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...


async def list_party_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...


CHOICE_GAME_HANDLERS = [
    CallbackQueryHandler(
        list_single_game,
        pattern=LIST_DUEL_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        list_duel_game,
        pattern=LIST_PARTY_GAME_CALLBACK_DATA
    ),
    CallbackQueryHandler(
        list_party_game,
        pattern=LIST_SINGLE_GAME_CALLBACK_DATA
    ),
]
