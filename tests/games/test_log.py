import unittest
from unittest.mock import MagicMock

from bot.games.log import Log
from bot.games.report import Report


class TestLog(unittest.TestCase):
    def setUp(self):
        self.mock_report1 = MagicMock(spec=Report)
        self.mock_report1.__str__ = MagicMock(return_value='Report 1')

        self.mock_report2 = MagicMock(spec=Report)
        self.mock_report2.__str__ = MagicMock(return_value='Report 2')

    def test_init_default(self):
        log = Log()

        self.assertEqual(log.size, 10)
        self.assertEqual(log.logs, [])

    def test_init_with_size(self):
        log = Log(size=5)

        self.assertEqual(log.size, 5)
        self.assertEqual(log.logs, [])

    def test_init_with_invalid_size(self):
        msg_error = 'size precisa ser maior que 0 (0).'
        with self.assertRaises(ValueError) as context:
            Log(size=0)

        self.assertEqual(str(context.exception), msg_error)

    def test_init_with_invalid_type_size(self):
        msg_error = "size precisa ser do tipo int (<class 'str'>)."
        with self.assertRaises(TypeError) as context:
            Log(size='invalid')

        self.assertEqual(str(context.exception), msg_error)

    def test_add_report(self):
        log = Log()

        self.assertEqual(len(log.logs), 0)

        log.add(self.mock_report1)

        self.assertEqual(len(log.logs), 1)
        self.assertIn(self.mock_report1, log.logs)

    def test_add_multiple_reports(self):
        log = Log()

        self.assertEqual(len(log.logs), 0)

        log.add(self.mock_report1)
        log.add(self.mock_report2)

        self.assertEqual(len(log.logs), 2)

    def test_size_limit(self):
        log = Log(size=2)
        mock_report3 = MagicMock(spec=Report)

        self.assertEqual(len(log.logs), 0)

        log.add(self.mock_report1)
        log.add(self.mock_report2)
        log.add(mock_report3)

        self.assertEqual(len(log.logs), 2)
        self.assertNotIn(self.mock_report1, log.logs)
        self.assertIn(self.mock_report2, log.logs)
        self.assertIn(mock_report3, log.logs)

    def test_iter(self):
        log = Log()
        log.add(self.mock_report1)
        log.add(self.mock_report2)

        reports = list(log)

        self.assertEqual(reports[0], self.mock_report2)
        self.assertEqual(reports[1], self.mock_report1)

    def test_str(self):
        log = Log()
        log.add(self.mock_report1)
        log.add(self.mock_report2)

        result = str(log)

        self.assertIn('02: Report 2', result)
        self.assertIn('01: Report 1', result)
