def escape_basic_markdown_v2(text: str):
    for char in r'_[](){}>#+-=|.!':
        escaped_char = f'\{char}'  # noqa
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text
