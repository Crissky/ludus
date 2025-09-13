import unittest

from unittest.mock import Mock

from bot.games.buttons.color_play_button import ColorPlayButton
from bot.games.enums.command import CommandEnum


class TestColorPlayButton(unittest.TestCase):

    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.id = 12345

    def test_inheritance(self):
        button = ColorPlayButton(
            text="Color Test",
            game=self.mock_game,
            command=CommandEnum.PLAY
        )

        self.assertEqual(button.text, "Color Test")
        self.assertEqual(button.game, self.mock_game)
        self.assertEqual(button.command, CommandEnum.PLAY)

    def test_make_button(self):
        button = ColorPlayButton("Color", self.mock_game, CommandEnum.PLAY)
        telegram_button = button.make_button()

        self.assertEqual(telegram_button.text, "Color")
        self.assertEqual(telegram_button.callback_data, button.data_to_str)
