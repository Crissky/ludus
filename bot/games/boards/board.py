from abc import ABC, abstractmethod
from typing import List

from bot.games.constants.text import NORMAL_SECTION_HEAD_1, TEXT_SEPARATOR_1
from bot.games.log import Log
from bot.games.player import Player
from bot.games.report import Report


class BaseBoard(ABC):
    def __init__(self, name: str, player_list: List[Player]):
        self.name = name
        self.player_list = player_list

        self.turn = 1
        self.is_clockwise = True
        self.player_turn = self.player_list[0]
        self.log = Log(self)

    def __str__(self):
        text = NORMAL_SECTION_HEAD_1.format(f'Game: {self.name}\n\n')
        for i, player in enumerate(self.player_list, start=1):
            text += f'{i}: {player}\n'
        text += TEXT_SEPARATOR_1
        return text

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

    @abstractmethod
    def player_options(self, player: Player = None):
        ...

    @abstractmethod
    def start_game(self):
        ...

    @abstractmethod
    def start_phase(self):
        ...

    @abstractmethod
    def play_phase(self):
        ...

    @abstractmethod
    def end_phase(self):
        ...

    def next_turn_phase(self):
        self.next_turn()

    def add_report(self, report: Report):
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

    @property
    def report(self):
        return Report(self.name, self.player_list)

    @property
    def total_players(self) -> int:
        return len(self.player_list)

    @property
    def game_header(self) -> str:
        return NORMAL_SECTION_HEAD_1.format(f'Game: {self.name}') + '\n\n'


if __name__ == '__main__':
    p1 = Player('0001', 'p1')
    p2 = Player('0002', 'p2')
    p3 = Player('0003', 'p3')
    p4 = Player('0004', 'p4')

    board = BaseBoard('test', [p1, p2, p3, p4])

    for i in range(10):
        print(f'Turno: {board.turn}, Vez: {board.player_turn}')
        board.next_turn()

    print('-'*79)

    board = BaseBoard('test', [p1, p2, p3, p4])
    board.is_clockwise = False

    for i in range(10):
        print(f'Turno: {board.turn}, Vez: {board.player_turn}')
        board.next_turn()
