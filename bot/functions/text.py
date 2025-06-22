from random import choice
from bot.constants.text import BASE_FOOTER, BASE_HEADER, BASE_HEADER_TEXT
from bot.functions.enums.emoji import FaceEmojiEnum, GameEmojiEnum


def escape_basic_markdown_v2(text: str):
    for char in r'_[](){}>#+-=|.!':
        escaped_char = f'\{char}'  # noqa
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text


def create_text_in_box(
    text: str,
    header_text: str = BASE_HEADER_TEXT,
    footer_text: str = BASE_HEADER_TEXT,
    header: str = BASE_HEADER,
    footer: str = BASE_FOOTER,
    header_emoji1: str = None,
    header_emoji2: str = None,
    footer_emoji1: str = None,
    footer_emoji2: str = None,
    clean_func: callable = escape_basic_markdown_v2,
) -> str:
    '''Cria um texto em uma caixa de texto.
    '''

    if header_emoji1 is None:
        header_emoji1 = get_random_game_emoji()
    if header_emoji2 is None:
        header_emoji2 = get_random_game_emoji()
    if footer_emoji1 is None:
        footer_emoji1 = get_random_game_emoji()
    if footer_emoji2 is None:
        footer_emoji2 = get_random_game_emoji()

    text = text.strip()
    header = header.format(
        text=header_text, emoji1=header_emoji1, emoji2=header_emoji2
    )
    footer = footer.format(
        text=footer_text, emoji1=footer_emoji1, emoji2=footer_emoji2
    )
    result = f'{header}\n\n{text}\n\n{footer}'
    if callable(clean_func):
        result = clean_func(result)

    return result


def get_random_refresh_text() -> str:
    emoji = choice(list(FaceEmojiEnum)).value
    return f'Atualizado{emoji}'


def get_random_game_emoji() -> str:
    emoji = choice(list(GameEmojiEnum)).value
    return f'{emoji}'
