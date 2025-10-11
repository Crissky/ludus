from typing import List, Optional

from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.decks.royal import RoyalDeck
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player


class GolfSolitaireBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = '🏌️‍♂️Golf Solitaire'
    DESCRIPTION: str = ('')

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = RoyalDeck()
        super().__init__(
            draw_pile,
            *players,
            is_shuffle_deck=True,
            total_discard_pile=1,
            discard_at_start=True,
            initial_hand_size=0,
            hand_kwargs={'max_size': 0},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.enemy = Player(player_id='0000000000', name='Solitaire')
        self.num_rows = 5
        self.num_card_per_row = 7
        self.board: List[Card] = []
        self.create_board()

        self.debug_attr_list.extend([
            'board',
        ])

    def get_card(self, row_index: int, card_index: int) -> Optional[Card]:
        '''Retorna uma carta da fileira. Mas retorna None de se
        se o row_index ou card_index passado estiver fora do range.
        '''

        if self.board is None:
            return None
        if row_index < 0 or row_index >= self.num_rows:
            return None
        if card_index < 0 or card_index >= self.num_card_per_row:
            return None

        row = self.board[row_index]
        card = row[card_index]

        return card

    def remove_card(self, row_index: int, card_index: int):
        '''Remove uma carta da fileira e a coloca na pilha de descarte.
        Levanta uma exceção se o row_index ou card_index estiver fora do range.
        '''

        card = self.get_card(row_index, card_index)
        if row_index < 0 or row_index >= self.num_rows:
            raise ValueError(f'Fileira {row_index} não existe.')
        if card_index < 0 or card_index >= self.num_card_per_row:
            raise ValueError(f'Coluna {card_index} não existe.')
        if card is None:
            raise ValueError(
                f'Carta na posição {row_index}x{card_index} já foi removida.'
            )
        if isinstance(card, Card):
            self.board[row_index][card_index] = None
            self.discard_piles[0].add(card)
        else:
            raise RuntimeError(
                'Não foi possível remover a carta na posição '
                f'{row_index}x{card_index}.'
            )

    def is_match_card(self, card1: Card, card2: Card) -> bool:
        '''Verifica se duas cartas "combinam", se elas tem valores sucesssor ou
        antecessor uma em relação a outra. Ex: 2 e 3, 10 e J, K e A, A e 2.

        Retorna True se as cartas são sucesssor/antecessor e False caso
        contrário.
        '''

        result = False
        value1 = card1.value
        value2 = card2.value
        max_value = len(card1.name.__class__) - 1

        if value1 == 0 and value2 == max_value:
            result = True
        elif value2 == 0 and value1 == max_value:
            result = True
        elif abs(value1 - value2) == 1:
            result = True

        return result

    def count_row(self, row_index: int) -> Optional[int]:
        '''Retorna o total de cartas da fileira. Mas retorna None de se
        se o row_index passado estiver fora do range.
        '''

        if row_index < 0 or row_index >= self.num_rows:
            return None

        row = self.board[row_index]
        return sum((1 for card in row if isinstance(card, Card)))

    def count_neighbors(self, row_index: int, card_index: int) -> int:
        '''Retorna o total de cartas vizinhas perpendiculares (cima, baixo,
        esquerda e direita).
        '''

        neighbors = [
            self.get_card(row_index + 1, card_index),
            self.get_card(row_index - 1, card_index),
            self.get_card(row_index, card_index + 1),
            self.get_card(row_index, card_index - 1),
        ]

        return sum((1 for neighbor in neighbors if isinstance(neighbor, Card)))

    def check_neighbors(self, row_index: int, card_index: int) -> dict:
        '''Retorna um dicionário com total de cartas vizinhas perpendiculares
        em relação aos vizinhos perpendiculares da carta passada.
        '''

        result = {}
        neighbors = {
            'n': (-1, 0),
            's': (1, 0),
            'e': (0, 1),
            'w': (0, -1),
        }

        for key, (ri, ci) in neighbors.items():
            neighbor_ri = row_index + ri
            neighbor_ci = card_index + ci
            neighbor_card = self.get_card(
                row_index=neighbor_ri,
                card_index=neighbor_ci
            )
            if isinstance(neighbor_card, Card):
                total = self.count_neighbors(
                    row_index=neighbor_ri,
                    card_index=neighbor_ci
                )
                result[neighbor_card.text] = total

        return result

    def create_board(self):
        '''Distribui cartas no tabuleiro.
        '''

        for _ in range(self.num_rows):
            row = []
            for _ in range(self.num_card_per_row):
                card_list = self.draw()
                row.extend(card_list)
            self.board.append(row)

    # ABSTRACT METHODS #######################################################
    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if self.is_started is not True:
            return self.invite_keyboard

        keyboard = PlayKeyBoard(buttons_per_row=self.num_card_per_row)
        if self.game_over:
            return keyboard

        for row_index, row in enumerate(self.board):
            for card_index, card in enumerate(row):
                text = text = card.text if card else '❌'
                callback_data_args = {
                    CallbackKeyEnum.ROW_INDEX.name: row_index,
                    CallbackKeyEnum.CARD_INDEX.name: card_index,
                }
                button = PlayButton(
                    text=text,
                    game=self,
                    command=CommandEnum.PLAY,
                    group=row_index,
                    **callback_data_args
                )
                keyboard.add_button(button)

        if self.draw_pile.is_empty is False:
            keyboard.add_button(self.draw_button)

        close_button = self.close_button
        help_button = self.help_button
        if isinstance(close_button, PlayButton):
            keyboard.add_button(close_button)
        if isinstance(help_button, PlayButton):
            keyboard.add_button(help_button)

        return keyboard

    def play(self, player: Player, play_dict: dict):
        result = super().play(player=player, play_dict=play_dict)
        if isinstance(result, str):
            return result

        command_str = play_dict[CallbackKeyEnum.COMMAND]
        command_enum = CommandEnum[command_str]

        if command_enum == CommandEnum.PLAY:
            row_index = play_dict.get(CallbackKeyEnum.ROW_INDEX)
            card_index = play_dict.get(CallbackKeyEnum.CARD_INDEX)
            card = self.get_card(row_index, card_index)
            if card is None:  # CHECA SE A CARTA EXISTE
                return 'Não há uma carta nessa casa para ser jogada.'

            total_neighbors = self.count_neighbors(row_index, card_index)
            if total_neighbors >= 4:
                return (
                    f'Carta "{card}" não pode ser jogada, pois ela está '
                    f'completamente cercada por {total_neighbors} cartas.'
                )

            top_card = self.top_discard_card
            is_match = self.is_match_card(card, top_card)
            if is_match is False:  # CHECA SE A CARTA COMBINA COM O DESCARTE
                value = top_card.value
                list_name = list(top_card.name.__class__)
                next_value = (value + 1) % len(list_name)
                previous_value = value - 1
                next_card_name = list_name[next_value].value
                previous_card_name = list_name[previous_value].value

                return (
                    f'Carta "{card}" não pode ser jogada. '
                    f'Jogue "{next_card_name}" ou "{previous_card_name}".'
                )

            total_board = self.total_board_cards
            if total_board > 2:  # CHECA SE VAI DEIXAR CARTA DESCONECTADA
                mid_row = self.num_rows // 2
                mid_col = self.num_card_per_row // 2
                if row_index <= mid_row:
                    vertical_card = self.get_card(
                        row_index=row_index-1,
                        card_index=card_index
                    )
                else:
                    vertical_card = self.get_card(
                        row_index=row_index+1,
                        card_index=card_index
                    )

                if card_index <= mid_col:
                    horizontal_card = self.get_card(
                        row_index=row_index,
                        card_index=card_index-1
                    )
                else:
                    horizontal_card = self.get_card(
                        row_index=row_index,
                        card_index=card_index+1
                    )

                if isinstance(vertical_card, Card):
                    return (
                        f'Carta "{card}" não pode ser jogada, '
                        f'pois "{vertical_card}" ficará desconectada.'
                    )
                if isinstance(horizontal_card, Card):
                    return (
                        f'Carta "{card}" não pode ser jogada, '
                        f'pois "{horizontal_card}" ficará desconectada.'
                    )

    def is_playable_card(self, card: Card) -> bool:
        return True

    def winners(self) -> List[Player]:
        winners = []
        if self.is_started is True and self.board:
            total_cards = sum((len(row) for row in self.board))
            if total_cards == 0:
                winners.append(self.player)
        elif not winners and self.draw_pile.is_empty:
            winners.append(self.enemy)

        return winners

    @property
    def player(self) -> Player:
        return self.player_list[0] if self.player_list else None

    @property
    def discard_pile(self) -> BaseDeck:
        if self.discard_piles:
            return self.discard_piles[0]
        else:
            return None

    @property
    def top_discard_card(self) -> Card:
        if self.discard_pile:
            card_list = self.discard_pile.peek(quantity=1)
            return card_list[0] if card_list else None
        else:
            return None

    @property
    def total_board_cards(self) -> int:
        count = 0
        for row in self.board:
            for card in row:
                if isinstance(card, Card):
                    count += 1

        return count
