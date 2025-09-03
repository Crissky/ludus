import unittest

from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from bot.games.report import Report
from bot.games.player import Player


class TestReport(unittest.TestCase):
    def setUp(self):
        self.action = "test action"
        self.player_name = "Test Player"
        self.player_id = "123"
        self.player = Player(player_id=self.player_id, name=self.player_name)
        self.mock_time = datetime(
            year=2023,
            month=1,
            day=1,
            hour=12,
            minute=30,
            second=0,
            tzinfo=timezone(timedelta(hours=-3))
        )
        self.mock_time_str = "12:30:00"

    @patch('bot.games.report.get_brazil_time_now')
    def test_report_init(self, mock_get_time):
        mock_get_time.return_value = self.mock_time

        report = Report(action=self.action, turn=1, player=self.player)

        self.assertEqual(report.action, self.action)
        self.assertEqual(report.turn, 1)
        self.assertEqual(report.player, self.player)
        self.assertEqual(report.created_at, self.mock_time_str)
        mock_get_time.assert_called_once()

    @patch('bot.games.report.get_brazil_time_now')
    def test_report_str_with_player_and_turn(self, mock_get_time):
        mock_get_time.return_value = self.mock_time

        report = Report(action=self.action, turn=1, player=self.player)
        report_str = str(report)

        self.assertIn(self.mock_time_str, report_str)
        self.assertIn(self.player_name, report_str)
        self.assertIn(self.action, report_str)

    @patch('bot.games.report.get_brazil_time_now')
    def test_report_str_without_player(self, mock_get_time):
        mock_get_time.return_value = self.mock_time

        report = Report(action=self.action, turn=1)
        report_str = str(report)

        self.assertIn(self.mock_time_str, report_str)
        self.assertIn(self.action, report_str)
        self.assertNotIn(self.player_name, report_str)

    @patch('bot.games.report.get_brazil_time_now')
    def test_report_str_without_turn(self, mock_get_time):
        mock_get_time.return_value = self.mock_time

        report = Report(action=self.action, turn=0, player=self.player)
        report_str = str(report)

        self.assertIn(self.mock_time_str, report_str)
        self.assertIn(self.player_name, report_str)
        self.assertIn(self.action, report_str)
        self.assertNotIn("Rodada: 00", report_str)

    @patch('bot.games.report.get_brazil_time_now')
    def test_report_repr(self, mock_get_time):
        mock_get_time.return_value = self.mock_time

        report = Report(action=self.action, turn=1, player=self.player)
        report_repr = repr(report)

        self.assertTrue(report_repr.startswith("Report("))
        self.assertIn(self.mock_time_str, report_repr)
        self.assertIn(self.player_name, report_repr)
        self.assertIn(self.action, report_repr)

    def test_report_action_invalid(self):
        msg_error = 'action precisa ser uma string.'
        with self.assertRaises(TypeError) as context:
            Report(action=123, turn=1, player=self.player)

        self.assertEqual(str(context.exception), msg_error)

    def test_report_turn_invalid(self):
        msg_error = 'turn precisa ser um inteiro.'
        with self.assertRaises(TypeError) as context:
            Report(action=self.action, turn='1', player=self.player)

        self.assertEqual(str(context.exception), msg_error)

    def test_report_player_invalid(self):
        msg_error = 'player precisa ser um Player ou None.'
        with self.assertRaises(TypeError) as context:
            Report(action=self.action, turn=1, player='player')

        self.assertEqual(str(context.exception), msg_error)
