import unittest
from unittest.mock import MagicMock

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.games.play_keyboard import PlayKeyBoard, InviteKeyBoard
from bot.games.buttons.play_button import PlayButton


class TestPlayKeyBoard(unittest.TestCase):
    def setUp(self):
        self.mock_button1 = MagicMock(spec=PlayButton)
        self.mock_button1.group = 0
        self.mock_button1.make_button.return_value = (
            InlineKeyboardButton("Test1", callback_data="test1")
        )

        self.mock_button2 = MagicMock(spec=PlayButton)
        self.mock_button2.group = 0
        self.mock_button2.make_button.return_value = (
            InlineKeyboardButton("Test2", callback_data="test2")
        )

    def test_init_default(self):
        keyboard = PlayKeyBoard()

        self.assertEqual(keyboard.buttons_per_row, 1)
        self.assertEqual(keyboard.play_button_list, [])

    def test_init_with_buttons_per_row(self):
        keyboard = PlayKeyBoard(buttons_per_row=2)

        self.assertEqual(keyboard.buttons_per_row, 2)

    def test_init_with_buttons(self):
        keyboard = PlayKeyBoard(1, self.mock_button1, self.mock_button2)

        self.assertEqual(len(keyboard.play_button_list), 2)

    def test_init_invalid_buttons_per_row(self):
        msg_error = 'O número de botões por linha deve ser maior que 0.'
        with self.assertRaises(ValueError) as context:
            PlayKeyBoard(buttons_per_row=0)

        self.assertEqual(str(context.exception), msg_error)

    def test_add_button(self):
        keyboard = PlayKeyBoard()

        keyboard.add_button(self.mock_button1)

        self.assertIn(self.mock_button1, keyboard.play_button_list)

    def test_add_duplicate_button(self):
        keyboard = PlayKeyBoard()
        keyboard.add_button(self.mock_button1)

        msg_error = 'Esse botão já está no teclado.'
        with self.assertRaises(ValueError) as context:
            keyboard.add_button(self.mock_button1)

        self.assertEqual(str(context.exception), msg_error)

    def test_add_invalid_button_type(self):
        keyboard = PlayKeyBoard()

        msg_error = (
            f'O botão deve ser uma instância de {PlayButton.__name__}.'
        )
        with self.assertRaises(ValueError) as context:
            keyboard.add_button("not_a_button")

        self.assertEqual(str(context.exception), msg_error)

    def test_make_buttons(self):
        keyboard = PlayKeyBoard(buttons_per_row=2)
        keyboard.add_button(self.mock_button1)
        keyboard.add_button(self.mock_button2)

        buttons = keyboard.make_buttons()

        self.assertEqual(len(buttons), 1)
        self.assertEqual(len(buttons[0]), 2)

    def test_make_keyboard(self):
        keyboard = PlayKeyBoard()
        keyboard.add_button(self.mock_button1)

        result = keyboard.make_keyboard()

        self.assertIsInstance(result, InlineKeyboardMarkup)

    def test_str(self):
        keyboard = PlayKeyBoard()
        self.mock_button1.__str__ = MagicMock(return_value="Button1")
        keyboard.add_button(self.mock_button1)

        result = str(keyboard)

        self.assertEqual(result, "Button1")

    def test_repr(self):
        keyboard = PlayKeyBoard(buttons_per_row=2)

        result = repr(keyboard)

        self.assertIn("PlayKeyBoard", result)
        self.assertIn("buttons_per_row=2", result)
