from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.scoundrel import ScoundrelCard
from bot.games.decks.deck import BaseDeck
from bot.games.decks.scoundrel import ScoundrelDeck
from bot.games.player import Player


class ScoundrelBoard(BaseCardGameBoard):
    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = ScoundrelDeck(is_shuffle=False)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=2,
            initial_hand_size=4,
            hand_kwargs={'max_size': 4},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.hp = 20
        self.debug_attr_list.extend([
            'hp',
            'field',
            'discard_pile',
        ])

    def discard(self, *cards: ScoundrelCard):
        if len(self.discard_piles) < 2:
            raise ValueError('Pilha de descarte não existe.')

        pile = self.discard_piles[1]
        pile.add(*cards)

    def put_field(self, *cards: ScoundrelCard):
        if len(self.discard_piles) < 1:
            raise ValueError('Campo não existe.')

        pile = self.discard_piles[0]
        pile.add(*cards)

    @property
    def field(self) -> BaseDeck:
        if self.discard_piles:
            return self.discard_piles[0]
        else:
            return None

    @property
    def discard_pile(self) -> BaseDeck:
        if self.discard_piles:
            return self.discard_piles[1]
        else:
            return None
