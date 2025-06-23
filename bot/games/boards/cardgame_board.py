import logging

from abc import abstractmethod
from typing import List

from bot.games.boards.board import BaseBoard
from bot.games.buttons.play_button import BasePlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
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
        hand_kwargs: dict = None
    ):
        super().__init__(*players)
        self.draw_pile = None
        self.discard_piles = None
        self.total_discard_pile = total_discard_pile
        self.initial_hand_size = initial_hand_size
        self.hand_kwargs = hand_kwargs

        if self.hand_kwargs is None:
            self.hand_kwargs = {}

        self.create_draw_pile(draw_pile)

    def create_draw_pile(self, draw_pile: BaseDeck):
        self.draw_pile = draw_pile
        # self.draw_pile.shuffle()

    def create_hands(self, player_list: List[Player], hand_kwargs: dict):
        for player in player_list:
            player_hand = BaseHand(**hand_kwargs)
            player.set_hand(player_hand)

    def distribute_cards(
        self,
        player_list: List[Player],
        initial_hand_size: int
    ):
        for _ in range(initial_hand_size):
            for player in player_list:
                card = self.draw()
                player.hand.add_card(card)

    def create_discard_pile(self, total_discard_pile: int):
        self.discard_piles = [BaseDeck() for _ in range(total_discard_pile)]

        for discard_pile in self.discard_piles:
            cards = self.draw()
            discard_pile.add(*cards)

    def draw(self, quantity: int = 1) -> List[Card]:
        cards = self.draw_pile.draw(quantity=quantity)
        if isinstance(cards, Card):
            cards = [cards]
        elif cards is None:
            cards = self.draw_when_empty(quantity=quantity)

        return cards

    def draw_when_empty(self, quantity: int = 1) -> List[Card]:
        raise ValueError('Sem cartas para comprar, pois o baralho está vazio.')

    def show_board(self) -> str:
        peek_discard_piles = ''
        if self.discard_piles is not None:
            peek_discard_piles = ', '.join((
                str(discard_pile.peek())
                for discard_pile in self.discard_piles
            ))

        text = self.game_header
        text += f'Turn: {self.turn}, Currrent Player: {self.player_turn}\n\n'
        text += f'Draw Pile: {len(self.draw_pile)}\n'
        text += f'Discard Pile: {peek_discard_piles}\n'

        for i, player in enumerate(self.player_list, start=1):
            quantity_hand = len(player)
            text += f'{i}: {player}, Hand: {quantity_hand}\n'
        text += f'\n{self.log}\n'

        return text

    def show_player_board(self, player: Player) -> str:
        text = self.game_header
        text += f'Player: {player.name}\n\n'
        text += f'{self.log}\n'

        return text

    # ABSTRACT METHODS
    def start_game(self):
        self.create_hands(self.player_list, self.hand_kwargs)
        self.distribute_cards(self.player_list, self.initial_hand_size)
        self.create_discard_pile(self.total_discard_pile)

    def player_options(self, player: Player = None) -> PlayKeyBoard:
        if player is None:
            player = self.player_turn

        keyboard = PlayKeyBoard(buttons_per_row=self.initial_hand_size)
        for index, card in enumerate(player):
            if self.is_playable_card(card=card):
                text = card.text
                button = BasePlayButton(
                    game=self,
                    text=text,
                    hand_position=index
                )
                keyboard.add_button(button)

        return keyboard

    def play(self):
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

    board.start_game()
    logging.debug(board.show_board())
    logging.debug('DRAW', '-'*74)

    board.draw()
    logging.debug(board.show_board())
    logging.debug('-'*79)
