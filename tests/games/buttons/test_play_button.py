import unittest
from unittest.mock import Mock

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
        with self.assertRaises(TypeError):
            PlayButton(
                text="Test",
                game=self.mock_game,
                command=123
            )

    def test_init_invalid_string_command(self):
        with self.assertRaises(KeyError):
            PlayButton(
                text="Test",
                game=self.mock_game,
                command="INVALID"
            )
