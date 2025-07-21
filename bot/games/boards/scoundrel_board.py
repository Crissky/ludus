from typing import List
from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.scoundrel_card import ScoundrelCard
from bot.games.decks.scoundrel import ScoundrelDeck
from bot.games.enums.card import RoyalSuits
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.player import Player


class ScoundrelBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = 'Scoundrel'
    DESCRIPTION: str = None

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = ScoundrelDeck(is_shuffle=False)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=2,
            discard_at_start=False,
            initial_hand_size=4,
            hand_kwargs={'max_size': 4},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.hp = 20
        self.max_hp = 20
        self.enemy = Player(name='Mestre da Masmorra')
        self.debug_attr_list.extend([
            'hp',
            'max_hp',
            'field',
            'discard_pile',
        ])

    def discard(self, *cards: ScoundrelCard) -> str:
        if len(self.discard_piles) < 2:
            raise ValueError('Pilha de descarte não existe.')

        pile = self.discard_piles[1]
        pile.add(*cards)
        action = f'Carta(s) descartada(s): {cards}.'

        return self.add_log(action=action, player=False)

    def put_in_field(self, *cards: ScoundrelCard) -> str:
        if len(self.discard_piles) < 1:
            raise ValueError('Campo não existe.')

        pile = self.discard_piles[0]
        pile.add(*cards)
        action = f'Carta(s) adicionada(s) ao campo: {cards}.'

        return self.add_log(action=action, player=False)

    def clean_field(self) -> str:
        quantity = len(self.field)
        card_list = self.field.draw(quantity=quantity)
        return self.discard(*card_list)

    def skip_room(self, player: Player) -> str:
        quantity = len(player.hand)
        card_list = player.hand.discard(quantity=quantity)
        self.draw_pile.add_bottom(*card_list)
        action = f'Carta(s) adicionada ao fim da Pilha de Compra: {card_list}.'

        return self.add_log(action=action, player=False)

    def play(self, player: Player, play_dict: dict):
        result = super().play(player=player, play_dict=play_dict)
        if isinstance(result, str):
            return result

        command_str = play_dict[CallbackKeyEnum.COMMAND]
        command_enum = CommandEnum[command_str]
        hand_position = play_dict.get(CallbackKeyEnum.HAND_POSITION)
        player = self.get_player(player)

        if command_enum == CommandEnum.PLAY:
            card_list = player.peek(hand_position)
            card = card_list[0] if card_list else None
            if not isinstance(card, ScoundrelCard):
                action = f'Carta na posição {hand_position} não encontrada.'
                return self.add_log(action=action, player=player)
            if not self.is_playable_card(card=card):
                action = f'Carta {card} não pode ser jogada.'
                return self.add_log(action=action, player=player)

    def is_playable_card(self, card: ScoundrelCard) -> bool:
        if not isinstance(card, ScoundrelCard):
            return False
        else:
            return True

    def winners(self) -> List[Player]:
        winners = []
        if self.hp > 0 and self.draw_pile.is_empty:
            winners = self.player_list.copy()
        elif self.hp <= 0:
            winners = [self.enemy]

        return winners

    @property
    def field(self) -> ScoundrelDeck:
        if self.discard_piles:
            return self.discard_piles[0]
        else:
            return None

    @property
    def discard_pile(self) -> ScoundrelDeck:
        if self.discard_piles:
            return self.discard_piles[1]
        else:
            return None

    @property
    def power(self) -> int:
        power = 0
        for card in self.field:
            if card.suit == RoyalSuits.DIAMONDS:
                power = card.value
            elif card.suit in (RoyalSuits.CLUBS, RoyalSuits.SPADES):
                if card.value > power:
                    power = 0

        return power
