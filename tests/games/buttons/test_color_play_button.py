import unittest

from unittest.mock import Mock

from bot.games.buttons.color_play_button import ColorPlayButton
from bot.games.enums.command import CommandEnum


class TestColorPlayButton(unittest.TestCase):

    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.id = 12345
