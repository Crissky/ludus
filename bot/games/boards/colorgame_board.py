from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.card import Card
from bot.games.decks.color import ColorDeck
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player


class ColorsGameBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = 'Colors'
    DESCRIPTION: str = None

    def __init__(self, *players: Player):
        draw_pile = ColorDeck(shuffle=False)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=1,
            initial_hand_size=7,
            hand_kwargs={},
            min_total_players=2,
            max_total_players=4,
        )
        self.pending_draw = 0
        self.selecting_color = False

    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if self.selecting_color is False or self.is_started is not True:
            return super().player_keyboard(player)

    def play(self, player: Player, play_dict: dict):
        command_str = play_dict[CallbackKeyEnum.COMMAND]
        command = CommandEnum[command_str]
        game_id = play_dict[CallbackKeyEnum.GAME_ID]
        hand_position = play_dict.get(CallbackKeyEnum.HAND_POSITION)
        # selected_color = play_dict.get(CallbackKeyEnum.SELECTED_COLOR)

        if game_id != self.id:
            action = f'Jogo inválido: {game_id}'
            return self.add_log(player=False, action=action)
        if player != self.current_player:
            action = f'Não é a vez de {player}.'
            return self.add_log(player=False, action=action)
        if not self.player_in_game(player):
            action = f'{player} não está mais no jogo.'
            return self.add_log(player=False, action=action)

        player = self.get_player(player)
        card = player.get_card(hand_position)

        if not isinstance(card, Card):
            action = f'Carta na posição {hand_position} não encontrada.'
            return self.add_log(player=False, action=action)

        if command == CommandEnum.PLAY:
            ...
        elif command == CommandEnum.DRAW:
            ...
        elif command == CommandEnum.PASS:
            ...
        elif command == CommandEnum.SELECT_COLOR:
            ...

    def is_playable_card(self, card: Card) -> bool:
        if not self.discard_piles:
            return True

        top_card = self.discard_piles[0].peek()

        # Testa o empilhamento de carta PLUS
        if self.pending_draw > 0:
            if card.plus_value > 0 and card.plus_value >= top_card.plus_value:
                return True
            return False

        # Caso normal: tem que bater cor ou nome
        if (
            card.suit == top_card.suit or
            card.name == top_card.name or
            card.is_wild
        ):
            return True

        return False
