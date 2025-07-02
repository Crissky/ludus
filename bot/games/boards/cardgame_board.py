import logging

from abc import abstractmethod
from typing import List

from bot.games.boards.board import BaseBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.enums.command import CommandEnum
from bot.games.hands.hand import BaseHand
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player


class BaseCardGameBoard(BaseBoard):
    DISPLAY_NAME: str = None
    DESCRIPTION: str = None

    def __init__(
        self,
        draw_pile: BaseDeck,
        *players: Player,
        total_discard_pile: int = 1,
        initial_hand_size: int = 7,
        hand_kwargs: dict = None,
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

        self.min_total_players = min_total_players
        self.max_total_players = max_total_players
        super().__init__(*players)

        self.draw_pile = None
        self.discard_piles = None
        self.total_discard_pile = total_discard_pile
        self.initial_hand_size = initial_hand_size
        self.hand_kwargs = hand_kwargs
        self.is_passing = False

        if self.hand_kwargs is None:
            self.hand_kwargs = {}

        self.create_draw_pile(draw_pile)

    def add_player(self, player: Player):
        if self.total_players >= self.max_total_players:
            action = (
                f'{player} não pode ser adicionado, '
                f'pois o limite de {self.max_total_players} jogadore(s) '
                'já foi atingido.'
            )
            return self.add_log(player=False, action=action)

        super().add_player(player)

    # CREATE FUNCTIONS #######################################################
    def create_draw_pile(self, draw_pile: BaseDeck):
        self.draw_pile = draw_pile
        # self.draw_pile.shuffle()

    def create_hands(self):
        for player in self.player_list:
            player_hand = BaseHand(**self.hand_kwargs)
            player.set_hand(player_hand)

    def create_discard_pile(self):
        self.discard_piles = [
            BaseDeck()
            for _ in range(self.total_discard_pile)
        ]

        for discard_pile in self.discard_piles:
            cards = self.draw()
            discard_pile.add(*cards)

    def distribute_cards(self):
        for _ in range(self.initial_hand_size):
            for player in self.player_list:
                card = self.draw()
                player.hand.add_card(card)

    def draw(self, quantity: int = 1) -> List[Card]:
        cards = self.draw_pile.draw(quantity=quantity)
        if isinstance(cards, Card):
            cards = [cards]
        elif cards is None:
            cards = self.draw_when_empty(quantity=quantity)

        return cards

    def draw_when_empty(self, quantity: int = 1) -> List[Card]:
        raise ValueError('Sem cartas para comprar, pois o baralho está vazio.')

    # SHOW BOARD FUNCTIONS ###################################################
    def show_board(self, player: Player = None) -> str:
        output = [self.game_header]
        if self.is_started is not True:
            output.append('Partida ainda não começou!\n')
        output.append(self.show_board_turn())
        output.append(self.show_board_draw_pile())
        output.append(self.show_board_discard_piles())

        output.append("\n🎮 Jogadores na partida:")
        for i, p in enumerate(self.player_list, start=1):
            marker = "👉" if p == self.current_player else "  "
            quantity_hand = len(p)
            output.append(f'{i:02}: {marker}{p}, Mão: {quantity_hand}')

        if player:
            output.append("\n🖐️ Suas cartas:")
            output.append(str(player.hand))

        output.append("\n📜 Últimas ações:")
        output.append(f'{self.log}')

        return '\n'.join(output)

    def show_board_draw_pile(self):
        return f'Pilha de Compra: {len(self.draw_pile)} carta(s)'

    def show_board_turn(self):
        return f'Rodada: {self.turn}'

    def show_board_discard_piles(self):
        peek_discard_piles = ''
        if self.discard_piles is not None:
            peek_discard_piles = ', '.join((
                str(discard_pile.peek()) if discard_pile else 'Pilha Vazia'
                for discard_pile in self.discard_piles
            ))

        return f'Pilha de Descarte: {peek_discard_piles}'

    # ABSTRACT METHODS #######################################################
    def start(self):
        if self.total_players < self.min_total_players:
            action = (
                'A partida só pode começar quando houver ao menos '
                f'{self.min_total_players} jogadores.'
            )
            return self.add_log(player=False, action=action)

        self.create_hands()
        self.distribute_cards()
        self.create_discard_pile()
        self.is_started = True
        self.turn = 1

    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        keyboard = PlayKeyBoard(buttons_per_row=self.initial_hand_size)
        if player != self.current_player:
            return keyboard

        for index, card in enumerate(player):
            if self.is_playable_card(card=card):
                text = card.text
                button = PlayButton(
                    game=self,
                    text=text,
                    command=CommandEnum.PLAY,
                    hand_position=index
                )
                keyboard.add_button(button)

        if self.is_passing is True:
            # Se is_passing é True, significa que o jogador já comprou nessa
            # rodada e não pode comprar novamente.
            button = PlayButton(
                game=self,
                text='🫴Passar',
                command=CommandEnum.PASS,
                group=1
            )
        else:
            button = PlayButton(
                game=self,
                text='🫴Comprar',
                command=CommandEnum.DRAW,
                group=1
            )
        keyboard.add_button(button)

        return keyboard

    def play(self, play_dict: dict):
        ...

    @abstractmethod
    def is_playable_card(self, card: Card) -> bool:
        ...


if __name__ == '__main__':
    from bot.games.decks.royal import RoyalDeck

    p1 = Player(player_id='0001', name='Player 1')
    p2 = Player(player_id='0002', name='Player 2')
    p3 = Player(player_id='0003', name='Player 3')
    p4 = Player(player_id='0004', name='Player 4')

    deck = RoyalDeck(shuffle=False)

    board = BaseCardGameBoard(
        deck,
        p1, p2, p3, p4
    )

    logging.debug(board.show_board())
    logging.debug('START GAME', '-'*68)

    board.start()
    logging.debug(board.show_board())
    logging.debug('DRAW', '-'*74)

    board.draw()
    logging.debug(board.show_board())
    logging.debug('-'*79)
