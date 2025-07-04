import logging

from abc import ABC, abstractmethod
from typing import Callable, Iterable, List, Union

from telegram import InlineKeyboardMarkup

from bot.games.constants.text import NORMAL_SECTION_HEAD_1, TEXT_SEPARATOR_1
from bot.games.log import Log
from bot.games.play_keyboard import InviteKeyBoard, PlayKeyBoard
from bot.games.player import Player
from bot.games.report import Report


class BaseBoard(ABC):
    DISPLAY_NAME: str = None
    DESCRIPTION: str = None

    def __init__(
        self,
        *players: Player,
        min_total_players: int = 1,
        max_total_players: int = 4,
    ):
        if min_total_players > max_total_players:
            raise ValueError(
                'O número mínimo de jogadores não pode ser '
                'maior que o número máximo. '
                f'(min_total_players: {min_total_players} e '
                f'max_total_players: {max_total_players}).'

            )
        elif min_total_players <= 0 or max_total_players <= 0:
            raise ValueError(
                'O número mínimo e máximo de jogadores deve ser maior que 0.'
            )

        self.id = id(self)
        self.turn = 0
        self.turn_direction = 1
        self.current_player_index = 0
        self.is_started = False
        self.log = Log()
        self.player_list: List[Player] = []
        self.invite_keyboard = InviteKeyBoard(None)
        self.invite_text_formatter: Callable = None
        self.play_text_formatter: Callable = None

        initial_report = Report(
            player=False,
            action=f'{self.DISPLAY_NAME} foi criado.',
            turn=self.turn
        )
        self.add_log(report=initial_report)

        # ARGS
        self.min_total_players = min_total_players
        self.max_total_players = max_total_players
        for player in players:
            self.add_player(player)

    def __str__(self) -> str:
        text = NORMAL_SECTION_HEAD_1.format(f'Game: {self.DISPLAY_NAME}')
        text += '\nJogadores:\n'
        for i, player in enumerate(self.player_list, start=1):
            text += f'{i}: {player}\n'
        # text += TEXT_SEPARATOR_1

        return text

    def __repr__(self) -> str:
        return f'Board({self.DISPLAY_NAME})'

    def add_player(self, player: Player):
        if not isinstance(player, Player):
            raise TypeError(f'Player {player} não é um Player.')

        action = None
        if self.player_in_game(player):
            action = (
                f'{player} já está na partida. '
                'Não é possível adicionar o mesmo jogador duas vezes.'
            )
        if self.total_players >= self.max_total_players:
            action = (
                f'{player} não pode ser adicionado, '
                f'pois o limite de {self.max_total_players} jogadore(s) '
                'já foi atingido.'
            )

        if action is not None:
            return self.add_log(player=False, action=action)

        self.player_list.append(player)
        action = f'{player.name} entrou na partida.'
        self.add_log(player=False, action=action)

    def set_invite_keyboard(
        self,
        keyboard: Union[InviteKeyBoard, InlineKeyboardMarkup]
    ):
        if not isinstance(keyboard, (InlineKeyboardMarkup, InviteKeyBoard)):
            raise TypeError(
                'Keyboard deve ser do tipo '
                f'{InlineKeyboardMarkup.__name__} ou '
                f'{InviteKeyBoard.__name__}.'
            )
        if isinstance(keyboard, InlineKeyboardMarkup):
            keyboard = InviteKeyBoard(keyboard=keyboard)
        self.invite_keyboard = keyboard

    def set_invite_text_formatter(self, formatter: Callable):
        '''Define função que formata o texto de convite, quando o jogo ainda
        não iniciou.
        '''

        if not callable(formatter):
            raise TypeError('Callback deve ser uma função.')

        self.invite_text_formatter = formatter

    def set_play_text_formatter(self, formatter: Callable):
        '''Define função que formata o texto quando o jogo já iniciou.
        '''

        if not callable(formatter):
            raise TypeError('Callback deve ser uma função.')

        self.play_text_formatter = formatter

    def player_in_game(self, player) -> bool:
        return player in self.player_list

    def remove_player(self, player: Player):
        if player not in self.player_list:
            raise ValueError(f'Player {player} não está no board.')
        if self.current_player == player:
            self.player_list.remove(player)
            self.set_next_player()
        else:
            self.player_list.remove(player)

    def next_turn(self):
        self.set_next_player()
        self.turn += 1

    def set_next_player(self, skip: bool = False):
        increment = 2 if skip is True else 1
        self.current_player_index = (
            self.current_player_index + increment * self.turn_direction
        ) % len(self.player_list)

    def invert_direction(self):
        self.turn_direction *= -1

    def add_log(
        self,
        report: Report = None,
        player: Player = None,
        action: str = None,
    ):
        if player is None and action is not None:
            player = self.current_player

        if player is not None and action is not None:
            report = Report(
                player=player,
                action=action,
                turn=self.turn
            )

        if isinstance(report, Report):
            logging.info(f'Adicionando log: {report}')
            self.log.add(report)

    def show_board(self, player: Player = None) -> str:
        output = [self.game_header]
        output.append(f'Rodada: {self.turn}')

        output.append("\n🎮 Jogadores na partida:")
        for i, player in enumerate(self.player_list, start=1):
            marker = "👉" if player == self.current_player else "  "
            output.append(f'{i}: {marker}{player}\n')

        if player:
            output.append("\n🖐️ Suas cartas:")
            output.append(str(player.hand))

        output.append("\n📜 Últimas ações:")
        output.append(f'{self.log}')
        output_text = self.format_show_board(output)

        return output_text

    def format_show_board(self, output: Iterable[str]):
        output_text = '\n'.join(output)
        if self.is_started is False and callable(self.invite_text_formatter):
            output_text = self.invite_text_formatter(output_text)
        elif self.is_started is True and callable(self.play_text_formatter):
            output_text = self.play_text_formatter(output_text)

        return output_text

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        ...

    @abstractmethod
    def play(self):
        ...

    @property
    def current_player(self) -> Player:
        if self.player_list:
            return self.player_list[self.current_player_index]
        else:
            logging.info(
                f'{self.__class__.__name__}.current_player: '
                f'Não há jogadores nessa board.'
            )
            return None

    @property
    def host(self) -> Player:
        return self.player_list[0] if self.player_list else None
    host_player = host

    @property
    def total_players(self) -> int:
        return len(self.player_list)

    @property
    def game_header(self) -> str:
        return NORMAL_SECTION_HEAD_1.format(
            f'Game - {self.DISPLAY_NAME}: {self.id}'
        ) + '\n'


if __name__ == '__main__':
    p1 = Player('0001', 'p1')
    p2 = Player('0002', 'p2')
    p3 = Player('0003', 'p3')
    p4 = Player('0004', 'p4')

    board = BaseBoard(*[p1, p2, p3, p4])

    for i in range(10):
        logging.debug(
            f'Turno: {board.turn}, Vez: {board.current_player}')
        board.next_turn()

    logging.debug('-'*79)

    board = BaseBoard(*[p1, p2, p3, p4])
    board.invert_direction()

    for i in range(10):
        logging.debug(
            f'Turno: {board.turn}, Vez: {board.current_player}')
        board.next_turn()
