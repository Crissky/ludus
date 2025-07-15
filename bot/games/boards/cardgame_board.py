import logging

from abc import abstractmethod
from typing import Callable, List

from bot.games.boards.board import BaseBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
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
        super().__init__(
            *players,
            min_total_players=min_total_players,
            max_total_players=max_total_players,
        )

        self.draw_pile: BaseDeck = None
        self.discard_piles: List[BaseDeck] = []
        self.total_discard_pile = total_discard_pile
        self.initial_hand_size = initial_hand_size
        self.hand_kwargs = hand_kwargs
        self.is_passing = False

        if self.hand_kwargs is None:
            self.hand_kwargs = {}

        self.create_draw_pile(draw_pile)

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
                card_list = self.draw()
                player.hand.add_card(*card_list)

    def draw(self, quantity: int = 1) -> List[Card]:
        cards = self.draw_pile.draw(quantity=quantity)

        if len(cards) < quantity:
            new_quantity = quantity - len(cards)
            new_cards = self.draw_when_empty(quantity=new_quantity)
            cards.extend(new_cards)

        return cards

    def draw_when_empty(self, quantity: int = 1) -> List[Card]:
        for pile in self.discard_piles:
            pile_length = len(pile)
            if pile_length > 1:
                top_card = pile.draw(quantity=1)
                pile_cards = pile.draw(quantity=pile_length)
                pile.add(*top_card)
                self.draw_pile.add(*pile_cards)

        cards = []
        if len(self.draw_pile) > quantity:
            cards = self.draw_pile.draw(quantity=quantity)

        return cards

    def draw_from_discard_piles(
        self,
        index_pile: int = 0,
        quantity: int = 1
    ) -> List[Card]:
        if index_pile < 0 or index_pile >= len(self.discard_piles):
            raise ValueError(f'Pilha de descarte {index_pile} não existe.')

        pile = self.discard_piles[index_pile]
        cards = pile.draw(quantity=quantity)

        return cards

    def discard(self, *cards: Card, index_pile: int = 0):
        if index_pile < 0 or index_pile >= len(self.discard_piles):
            raise ValueError(f'Pilha de descarte {index_pile} não existe.')

        pile = self.discard_piles[index_pile]
        pile.add(*cards)

    # SHOW BOARD FUNCTIONS ###################################################
    def show_board(
        self,
        player: Player = None,
        general_info_list: List[Callable] = None
    ) -> str:
        if general_info_list is None:
            general_info_list = []

        output = [self.game_header]
        if self.is_started is not True:
            output.append('Partida ainda não começou!\n')

        # INFORMAÇÕES GERAIS
        output.append(self.show_board_turn())
        output.append(self.show_board_winner())
        output.append(self.show_board_draw_pile())
        output.append(self.show_board_discard_piles())
        for general_info in general_info_list:
            output.append(general_info())

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
        output_text = self.format_show_board(output)

        return output_text

    def show_board_turn(self):
        return f'Rodada: {self.turn}'

    def show_board_winner(self):
        winners = self.winners()
        text = None
        if winners:
            text = 'Vencedor(es): '
            text += ', '.join(str(winner) for winner in winners)

        return text

    def show_board_draw_pile(self):
        return f'Pilha de Compra: {len(self.draw_pile)} carta(s)'

    def show_board_discard_piles(self):
        peek_discard_piles = ', '.join((
            str(discard_pile.peek()[0]) if discard_pile else 'Vazia'
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
            return self.add_log(action=action, player=False)

        self.create_hands()
        self.distribute_cards()
        self.create_discard_pile()
        self.is_started = True
        self.turn = 1

    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if self.is_started is not True:
            return self.invite_keyboard

        keyboard = PlayKeyBoard(buttons_per_row=self.initial_hand_size)
        if player != self.current_player:
            return keyboard
        if self.game_over:
            return keyboard

        for index, card in enumerate(player):
            if self.is_playable_card(card=card):
                text = card.text
                callback_data_args = {
                    CallbackKeyEnum.HAND_POSITION.name: index,
                }
                button = PlayButton(
                    text=text,
                    game=self,
                    command=CommandEnum.PLAY,
                    **callback_data_args

                )
                keyboard.add_button(button)

        if self.is_passing is True:
            # Se is_passing é True, significa que o jogador já comprou nessa
            # rodada e não pode comprar novamente.
            button = PlayButton(
                text='🫴Passar',
                game=self,
                command=CommandEnum.PASS,
                group=1
            )
        else:
            button = PlayButton(
                text='🫴Comprar',
                game=self,
                command=CommandEnum.DRAW,
                group=1
            )
        keyboard.add_button(button)

        return keyboard

    @abstractmethod
    def play(self, player: Player, play_dict: dict):
        ...

    @abstractmethod
    def is_playable_card(self, card: Card) -> bool:
        ...

    @abstractmethod
    def winners(self) -> List[Player]:
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
