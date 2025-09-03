import unittest

from unittest.mock import MagicMock

from telegram import User

from bot.games.player import Player
from bot.games.hands.hand import BaseHand
from bot.games.cards.card import Card


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.mock_user = MagicMock(spec=User)
        self.mock_user.id = 123
        self.mock_user.name = 'Test User'
        self.mock_card = MagicMock(spec=Card)
        self.mock_hand = MagicMock(spec=BaseHand)

    def test_init_with_player_id_and_name(self):
        player_id = '123'
        player_name = 'Test Player'
        player = Player(player_id=player_id, name=player_name)

        self.assertEqual(player.id, player_id)
        self.assertEqual(player.name, player_name)
        self.assertIsInstance(player.hand, BaseHand)
        self.assertIsNone(player.message_id)

    def test_init_with_user(self):
        player = Player(user=self.mock_user)

        self.assertEqual(player.id, '123')
        self.assertEqual(player.name, 'Test User')
        self.assertIsInstance(player.hand, BaseHand)

    def test_init_with_hand(self):
        player_id = '123'
        player_name = 'Test Player'
        player = Player(
            player_id=player_id, name=player_name,
            hand=self.mock_hand
        )

        self.assertEqual(player.id, player_id)
        self.assertEqual(player.name, player_name)
        self.assertEqual(player.hand, self.mock_hand)

    def test_init_with_message_id(self):
        player_id = '123'
        player_name = 'Test Player'
        message_id = 456
        player = Player(
            player_id=player_id,
            name=player_name,
            message_id=message_id
        )

        self.assertEqual(player.id, player_id)
        self.assertEqual(player.name, player_name)
        self.assertEqual(player.message_id, message_id)

    def test_init_invalid_no_params(self):
        msg_error = 'player_id e name ou user devem ser informados.'
        with self.assertRaises(ValueError) as context:
            Player()

        self.assertEqual(str(context.exception), msg_error)

    def test_init_invalid_player_id_type(self):
        msg_error = 'player_id precisa ser do tipo int ou str.'
        with self.assertRaises(TypeError) as context:
            Player(player_id=[], name="Test")

        self.assertEqual(str(context.exception), msg_error)

    def test_init_invalid_name_type(self):
        msg_error = 'name precisa ser do tipo str.'
        with self.assertRaises(TypeError) as context:
            Player(player_id="123", name=123)

        self.assertEqual(str(context.exception), msg_error)

    def test_init_invalid_user_type(self):
        msg_error = 'user precisa ser do tipo User.'
        with self.assertRaises(TypeError) as context:
            Player(user="not_user")

        self.assertEqual(str(context.exception), msg_error)

    def test_init_invalid_hand_type(self):
        msg_error = 'hand precisa ser do tipo BaseHand.'
        with self.assertRaises(TypeError) as context:
            Player(player_id="123", name="Test", hand="not_hand")

        self.assertEqual(str(context.exception), msg_error)

    def test_init_invalid_message_id_type(self):
        msg_error = 'message_id precisa ser do tipo int.'
        with self.assertRaises(TypeError) as context:
            Player(player_id="123", name="Test", message_id="not_int")

        self.assertEqual(str(context.exception), msg_error)

    def test_eq_with_player(self):
        player1 = Player(player_id="123", name="Test1")
        player2 = Player(player_id="123", name="Test2")
        player3 = Player(player_id="456", name="Test3")

        self.assertEqual(player1, player2)
        self.assertNotEqual(player1, player3)

    def test_eq_with_user(self):
        player = Player(player_id="123", name="Test")

        self.assertEqual(player, self.mock_user)

    def test_eq_with_int_str(self):
        player = Player(player_id="123", name="Test")

        self.assertEqual(player, 123)
        self.assertEqual(player, "123")

    def test_hash(self):
        player = Player(player_id="123", name="Test")

        self.assertEqual(hash(player), hash("123"))

    def test_str(self):
        player = Player(player_id="123", name="Test Player")

        self.assertEqual(str(player), "Test Player")

    def test_repr(self):
        player = Player(player_id="123", name="Test Player", message_id=456)

        expected = "Player(id=123, name=Test Player, message_id=456)"
        self.assertEqual(repr(player), expected)

    def test_set_hand(self):
        player = Player(player_id="123", name="Test")

        player.set_hand(self.mock_hand)

        self.assertEqual(player.hand, self.mock_hand)

    def test_set_hand_invalid_type(self):
        player = Player(player_id="123", name="Test")

        msg_error = 'hand precisa ser do tipo BaseHand.'
        with self.assertRaises(TypeError) as context:
            player.set_hand("not_hand")

        self.assertEqual(str(context.exception), msg_error)

    def test_add_card(self):
        player = Player(player_id="123", name="Test")
        player.hand.add_card = MagicMock(return_value=[])

        result = player.add_card(self.mock_card)

        player.hand.add_card.assert_called_once_with(
            self.mock_card, discard_index=-1)
        self.assertEqual(result, [])

    def test_discard(self):
        player = Player(player_id="123", name="Test")
        player.hand.discard = MagicMock(return_value=[self.mock_card])

        result = player.discard(0, 1)

        player.hand.discard.assert_called_once_with(index=0, quantity=1)
        self.assertEqual(result, [self.mock_card])

    def test_play(self):
        player = Player(player_id="123", name="Test")
        player.hand.play = MagicMock(return_value=[self.mock_card])

        result = player.play(0, 1)

        player.hand.play.assert_called_once_with(0, 1)
        self.assertEqual(result, [self.mock_card])

    def test_peek(self):
        player = Player(player_id="123", name="Test")
        player.hand.peek = MagicMock(return_value=[self.mock_card])

        result = player.peek(0, 1)

        player.hand.peek.assert_called_once_with(0, 1)
        self.assertEqual(result, [self.mock_card])

    def test_set_message_id(self):
        player = Player(player_id="123", name="Test")

        player.set_message_id(789)

        self.assertEqual(player.message_id, 789)

    def test_set_message_id_invalid_type(self):
        player = Player(player_id="123", name="Test")

        meg_error = 'message_id precisa ser do tipo int.'
        with self.assertRaises(TypeError) as context:
            player.set_message_id("not_int")

        self.assertEqual(str(context.exception), meg_error)

    def test_user_id_property(self):
        player = Player(player_id="123", name="Test")

        self.assertEqual(player.user_id, "123")

    def test_player_id_property(self):
        player = Player(player_id="123", name="Test")

        self.assertEqual(player.player_id, "123")

    def test_user_name_property(self):
        player = Player(player_id="123", name="Test Player")

        self.assertEqual(player.user_name, "Test Player")
