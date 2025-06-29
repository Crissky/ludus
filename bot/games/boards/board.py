import logging

from abc import ABC, abstractmethod
from typing import List

from bot.games.constants.text import NORMAL_SECTION_HEAD_1, TEXT_SEPARATOR_1
from bot.games.log import Log
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player
from bot.games.report import Report


class BaseBoard(ABC):
    DISPLAY_NAME: str = None
    DESCRIPTION: str = None

    def __init__(self, *players: Player):
        self.id = id(self)
        self.player_list: List[Player] = []
        self.turn = 0
        self.turn_direction = 1
        self.current_player_index = 0
        self.is_started = False
        self.log = Log()

        initial_report = Report(
            player=False,
            action=f'{self.DISPLAY_NAME} foi criado.',
            turn=self.turn
        )
        self.add_log(report=initial_report)
        for player in players:
            self.add_player(player)

    def __str__(self):
        text = NORMAL_SECTION_HEAD_1.format(f'Game: {self.DISPLAY_NAME}\n\n')
        for i, player in enumerate(self.player_list, start=1):
            text += f'{i}: {player}\n'
        text += TEXT_SEPARATOR_1
        return text

    def __repr__(self):
        return f'Board({self.DISPLAY_NAME})'

    def add_player(self, player: Player):
        if player in self.player_list:
            action = (
                f'{player} já está na partida. '
                'Não é possível adicionar o mesmo jogador duas vezes.'
            )
            self.add_log(player=False, action=action)
            return
        if not isinstance(player, Player):
            raise TypeError(f'Player {player} não é um Player.')

        self.player_list.append(player)
        action = f'{player.name} entrou na partida.'
        self.add_log(player=False, action=action)

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
        output.append(f'Turn: {self.turn}')
        output.append("\n🎮 Jogadores na partida:")

        for i, player in enumerate(self.player_list, start=1):
            marker = "👉" if player == self.current_player else "  "
            output.append(f'{i}: {marker}{player}\n')

        if player is not None:
            output.append("\n🖐️ Suas cartas:")
            output.append(str(player.hand))

        output.append("\n📜 Últimas ações:")
        output.append(f'{self.log}')

        return '\n'.join(output)

    @abstractmethod
    def start_game(self):
        ...

    @abstractmethod
    def player_keyboard(self, player: Player = None) -> PlayKeyBoard:
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
