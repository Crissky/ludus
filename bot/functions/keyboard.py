from typing import List

from telegram import InlineKeyboardButton

from bot.constants.callback import MAIN_MENU_GAME_CALLBACK_DATA


def reshape_row_buttons(
    buttons: List[InlineKeyboardButton],
    buttons_per_row: int = 2
) -> List[List[InlineKeyboardButton]]:
    ''' Transforma uma lista de botões em uma lista de listas de botões,
    com um número de botões por linha definido pelo parâmetro buttons_per_row.

    Por exemplo, se buttons_per_row for 2, então será gerada uma lista com
    listas de botões, onde cada lista de botões terá no máximo 2 botões.
    '''

    final_buttons = []
    total_buttons = len(buttons)
    for i in range(0, total_buttons, buttons_per_row):
        final_buttons.append(buttons[i:i + buttons_per_row])

    return final_buttons


def get_back_button(
    callback_data: str = MAIN_MENU_GAME_CALLBACK_DATA
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text='↩️ Voltar',
        callback_data=callback_data
    )
