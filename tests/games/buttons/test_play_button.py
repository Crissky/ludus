import unittest
from unittest.mock import Mock

from bot.games.buttons.play_button import PlayButton
from bot.games.enums.command import CallbackKeyEnum, CommandEnum


class TestPlayButton(unittest.TestCase):

    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.id = 12345
