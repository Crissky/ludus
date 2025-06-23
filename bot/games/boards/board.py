import logging

from abc import ABC, abstractmethod

from bot.games.constants.text import NORMAL_SECTION_HEAD_1, TEXT_SEPARATOR_1
from bot.games.log import Log
from bot.games.player import Player
from bot.games.report import Report


class BaseBoard(ABC):
    DISPLAY_NAME: str = None
    DESCRIPTION: str = None

    def __init__(self, *players: Player):
        self.id = id(self)
        self.player_list = []

        for player in players:
            self.add_player(player)

        self.turn = 1
        self.is_clockwise = True
        self.player_turn = self.player_list[0]
        self.log = Log()

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
            raise ValueError(f'Player {player} já está no board.')
        if not isinstance(player, Player):
            raise TypeError(f'Player {player} não é um Player.')

        self.player_list.append(player)

    def remove_player(self, player: Player):
        if player not in self.player_list:
            raise ValueError(f'Player {player} não está no board.')
        if self.player_turn == player:
            self.set_next_player()

        self.player_list.remove(player)

    def next_turn(self):
        self.turn += 1
        self.set_next_player()

    def set_next_player(self):
        current_player_index = self.player_list.index(self.player_turn)
        if self.is_clockwise:
            next_player_index = (current_player_index + 1) % self.total_players
        else:
            next_player_index = (current_player_index - 1) % self.total_players
        self.player_turn = self.player_list[next_player_index]

    def inverter_turn(self):
        self.is_clockwise = not self.is_clockwise

    def next_turn_phase(self):
        self.next_turn()

    def add_log(
        self,
        report: Report = None,
        player: Player = None,
        action: str = None,
    ):
        if player is None and action is not None:
            player = self.player_turn

        if player is not None and action is not None:
            report = Report(
                game_id=self.id,
                player=player,
                action=action,
                turn=self.turn
            )

        self.log.add(report)

    def show_board(self) -> str:
        text = self.game_header
        text += f'Turn: {self.turn}, Currrent Player: {self.player_turn}\n\n'
        for i, player in enumerate(self.player_list, start=1):
            text += f'{i}: {player}\n'
        text += f'\n{self.log}\n'

        return text

    def show_player_board(self, player: Player) -> str:
        text = self.game_header
        text += f'Player: {player.name}\n\n'
        text += f'{self.log}\n'

        return text

    @abstractmethod
    def start_game(self):
        ...

    @abstractmethod
    def player_options(self, player: Player = None):
        ...

    @abstractmethod
    def play(self):
        ...

    @property
    def report(self):
        return Report(self.name, self.player_list)

    @property
    def total_players(self) -> int:
        return len(self.player_list)

    @property
    def game_header(self) -> str:
        return NORMAL_SECTION_HEAD_1.format(
            f'Game: {self.DISPLAY_NAME}'
        ) + '\n\n'


if __name__ == '__main__':
    p1 = Player('0001', 'p1')
    p2 = Player('0002', 'p2')
    p3 = Player('0003', 'p3')
    p4 = Player('0004', 'p4')

    board = BaseBoard(*[p1, p2, p3, p4])

    for i in range(10):
        logging.debug(f'Turno: {board.turn}, Vez: {board.player_turn}')
        board.next_turn()

    logging.debug('-'*79)

    board = BaseBoard(*[p1, p2, p3, p4])
    board.is_clockwise = False

    for i in range(10):
        logging.debug(f'Turno: {board.turn}, Vez: {board.player_turn}')
        board.next_turn()
