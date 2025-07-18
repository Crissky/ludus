from bot.functions.date_time import get_brazil_time_now
from bot.games.player import Player


class Report:
    def __init__(
        self,
        action: str,
        turn: int,
        player: Player = None,
    ):
        if not isinstance(action, str):
            raise TypeError('action precisa ser uma string.')
        if not isinstance(turn, int):
            raise TypeError('turn precisa ser um inteiro.')
        if not isinstance(player, Player) and player is not None:
            raise TypeError('player precisa ser um Player ou None.')

        self.action = action
        self.turn = turn
        self.player = player
        self.created_at = get_brazil_time_now().strftime('%H:%M:%S')

    def __str__(self):
        text = f'{self.created_at} - '
        if isinstance(self.turn, int) and self.turn > 0:
            f'Rodada: {self.turn:02} - '

        if isinstance(self.player, Player):
            text += f'{self.player}: {self.action}'
        else:
            text += f'{self.action}'

        return text

    def __repr__(self):
        return f'Report({self})'
