from random import choice
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.functions.enums.emoji import EmojiEnum, FaceEmojiEnum


CALLBACK_CLOSE = '$close'
LEFT_CLOSE_BUTTON_TEXT = f'{EmojiEnum.CLOSE.value}Fechar'
RIGHT_CLOSE_BUTTON_TEXT = f'Fechar{EmojiEnum.CLOSE.value}'
REFRESH_BUTTON_TEXT = f'{EmojiEnum.REFRESH.value}Atualizar'
DETAIL_BUTTON_TEXT = f'{EmojiEnum.DETAIL.value}Detalhar'


# BUTTONS FUNCTIONS
def get_close_button(
    user_id: int = None,
    text: str = None,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    '''Se user_id for None, qualquer um pode fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar fechar
    a mensagem.
    '''

    if text is None:
        text = LEFT_CLOSE_BUTTON_TEXT
        if right_icon:
            text = RIGHT_CLOSE_BUTTON_TEXT

    return InlineKeyboardButton(
        text=text,
        callback_data=(
            f'{{"command":"{CALLBACK_CLOSE}",'
            f'"user_id":{user_id}}}'
        )
    )


def get_refresh_close_button(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> List[InlineKeyboardButton]:
    '''Se user_id for None, qualquer um pode fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar fechar
    a mensagem.
    '''

    button_list = []
    button_list.append(
        InlineKeyboardButton(
            REFRESH_BUTTON_TEXT,
            callback_data=(
                f'{{"{refresh_data}":1,'
                f'"user_id":{user_id}}}'
            )
        )
    )
    if to_detail:
        button_list.append(
            InlineKeyboardButton(
                DETAIL_BUTTON_TEXT,
                callback_data=(
                    f'{{"{refresh_data}":1,"verbose":"v",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    button_list.append(get_close_button(user_id=user_id, right_icon=True))

    return button_list


def get_random_refresh_text() -> str:
    emoji = choice(list(FaceEmojiEnum)).value
    return f'Atualizado{emoji}'


def get_close_keyboard(user_id: int) -> InlineKeyboardMarkup:
    '''Se user_id for None, qualquer um pode fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar fechar
    a mensagem.
    '''

    return InlineKeyboardMarkup([[
        get_close_button(user_id=user_id)
    ]])


def get_refresh_close_keyboard(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> InlineKeyboardMarkup:
    '''Se user_id for None, qualquer um pode fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar fechar
    a mensagem.
    '''

    return InlineKeyboardMarkup([
        get_refresh_close_button(
            user_id=user_id,
            refresh_data=refresh_data,
            to_detail=to_detail
        )
    ])
