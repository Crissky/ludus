import unittest

from unittest.mock import Mock

from telegram import InlineKeyboardButton

from bot.games.buttons.play_button import PlayButton
from bot.games.enums.command import CallbackKeyEnum, CommandEnum


class TestPlayButton(unittest.TestCase):

    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.id = 12345

    def test_init_with_command_enum(self):
        button = PlayButton(
            text="Test",
            game=self.mock_game,
            command=CommandEnum.PLAY
        )

        self.assertEqual(button.text, "Test")
        self.assertEqual(button.game, self.mock_game)
        self.assertEqual(button.command, CommandEnum.PLAY)
        self.assertEqual(button.group, 0)

    def test_init_with_string_command(self):
        button = PlayButton(
            text="Test",
            game=self.mock_game,
            command="PLAY"
        )

        self.assertEqual(button.text, "Test")
        self.assertEqual(button.game, self.mock_game)
        self.assertEqual(button.command, CommandEnum.PLAY)
        self.assertEqual(button.group, 0)

    def test_init_invalid_command_type(self):
        msg_error = (
            'Command precisa ser uma instância de CommandEnum ou uma '
            'string válida de CommandEnum.'
        )
        with self.assertRaises(TypeError) as context:
            PlayButton(
                text="Test",
                game=self.mock_game,
                command=123
            )

        self.assertEqual(str(context.exception), msg_error)

    def test_init_invalid_string_command(self):
        msg_error = "'INVALID'"
        with self.assertRaises(KeyError) as context:
            PlayButton(
                text="Test",
                game=self.mock_game,
                command="INVALID"
            )

        self.assertEqual(str(context.exception), msg_error)

    def test_callback_data_validation_valid(self):
        button = PlayButton(
            "Test",
            self.mock_game,
            CommandEnum.PLAY,
            HAND_POSITION=1
        )
        self.assertEqual(button.callback_data["HAND_POSITION"], 1)

    def test_callback_data_validation_invalid(self):
        msg_error = (
            "callback_data inválido(s): ['INVALID_KEY'].\n"
            "Os valores válidos são: "
            "['COMMAND', 'GAME_ID', 'HAND_POSITION', 'DISCARD_POSITION', "
            "'SELECTED_COLOR', 'ROW_INDEX', 'CARD_INDEX']."
        )
        with self.assertRaises(ValueError) as context:
            PlayButton(
                "Test",
                self.mock_game,
                CommandEnum.PLAY,
                INVALID_KEY=1
            )

        self.assertEqual(str(context.exception), msg_error)

    def test_equality(self):
        button1 = PlayButton("Test", self.mock_game, CommandEnum.PLAY)
        button2 = PlayButton("Test", self.mock_game, CommandEnum.PLAY)

        self.assertEqual(button1, button2)

    def test_inequality_different_command(self):
        button1 = PlayButton("Test", self.mock_game, CommandEnum.PLAY)
        button2 = PlayButton("Test", self.mock_game, CommandEnum.DRAW)

        self.assertNotEqual(button1, button2)

    def test_str_representation(self):
        button = PlayButton("Test Button", self.mock_game, CommandEnum.PLAY)

        self.assertEqual(str(button), "Test Button")

    def test_callback_data_to_string(self):
        data = {CallbackKeyEnum.COMMAND: "PLAY", CallbackKeyEnum.GAME_ID: 123}
        result = PlayButton.callback_data_to_string(data)

        self.assertIn("0:", result)  # COMMAND index
        self.assertIn('"PLAY"', result)  # COMMAND index
        self.assertIn("1:", result)  # GAME_ID index
        self.assertIn("123", result)  # GAME_ID index

    def test_callback_data_to_dict(self):
        original_data = {
            CallbackKeyEnum.COMMAND: "PLAY",
            CallbackKeyEnum.GAME_ID: 123
        }
        string_data = PlayButton.callback_data_to_string(original_data)
        result = PlayButton.callback_data_to_dict(string_data)

        self.assertEqual(result[CallbackKeyEnum.COMMAND], "PLAY")
        self.assertEqual(result[CallbackKeyEnum.GAME_ID], 123)

    def test_callback_data_to_pattern(self):
        pattern = PlayButton.callback_data_to_pattern(CommandEnum.PLAY)

        self.assertIsInstance(pattern, str)
        self.assertIn("0:", pattern)

    def test_callback_data_to_pattern_with_string(self):
        pattern = PlayButton.callback_data_to_pattern("PLAY")

        self.assertIsInstance(pattern, str)
        self.assertIn("0:", pattern)

    def test_callback_data_to_pattern_invalid_type(self):
        msg_error = (
            'Command precisa ser uma instância de CommandEnum ou uma '
            'striing válida de CommandEnum.'
        )
        with self.assertRaises(TypeError) as context:
            PlayButton.callback_data_to_pattern(123)

        self.assertEqual(str(context.exception), msg_error)

    def test_data_to_str_property(self):
        button = PlayButton("Test", self.mock_game, CommandEnum.PLAY)
        result = button.data_to_str

        self.assertIsInstance(result, str)
        self.assertIn("{", result)
        self.assertIn("}", result)
        self.assertIn("PLAY", result)
        self.assertIn("12345", result)

    def test_make_button(self):
        button = PlayButton("Test", self.mock_game, CommandEnum.PLAY)
        telegram_button = button.make_button()

        self.assertIsInstance(telegram_button, InlineKeyboardButton)
        self.assertEqual(telegram_button.text, "Test")
        self.assertEqual(telegram_button.callback_data, button.data_to_str)
