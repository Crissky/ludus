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
        self.healed_this_turn = False
        self.debug_attr_list.extend([
            'hp',
            'max_hp',
            'field',
            'discard_pile',
        ])

    def discard(self, *cards: ScoundrelCard) -> str:
        if self.discard_pile is None:
            raise ValueError('Pilha de descarte não existe.')

        pile = self.discard_pile
        pile.add(*cards)
        action = f'Carta(s) descartada(s): {cards}.'

        return self.add_log(action=action, player=False)

    def put_in_field(self, *cards: ScoundrelCard) -> str:
        if self.field_pile is None:
            raise ValueError('Campo não existe.')

        pile = self.field_pile
        pile.add(*cards)
        action = f'Carta(s) adicionada(s) ao campo: {cards}.'

        return self.add_log(action=action, player=False)

    def clean_field(self) -> str:
        quantity = len(self.field_pile)
        card_list = self.field_pile.draw(quantity=quantity)
        return self.discard(*card_list)

    def skip_room(self, player: Player) -> str:
        quantity = len(player.hand)
        card_list = player.hand.discard(quantity=quantity)
        self.draw_pile.add_bottom(*card_list)
        action = f'Carta(s) adicionada ao fim da Pilha de Compra: {card_list}.'

        return self.add_log(action=action, player=False)

    def damage_hp(self, value: int) -> str:
        self.hp -= value
        self.hp = max(self.hp, 0)
        action = f'Perdeu {value} pontos de dano.'

        return self.add_log(action=action, player=False)

    def heal_hp(self, value: int) -> str:
        self.hp += value
        self.hp = min(self.hp, self.max_hp)
        self.healed_this_turn = True
        action = f'Recuperou {value} pontos de vida.'

        return self.add_log(action=action, player=False)

    def next_turn(self, player: Player, skip: bool = False):
        self.turn += 1
        if skip is False:
            action = f'Está indo para a sala {self.turn}.'
        else:
            action = 'Evitou a sala.'

        self.add_log(action=action, player=player)

    def show_board_turn(self) -> str:
        return f'Sala: {self.turn}'

    def play(self, player: Player, play_dict: dict):
        result = super().play(player=player, play_dict=play_dict)
        if isinstance(result, str):
            return result

        command_str = play_dict[CallbackKeyEnum.COMMAND]
        command_enum = CommandEnum[command_str]
        hand_position = play_dict.get(CallbackKeyEnum.HAND_POSITION)
        player = self.get_player(player)

        if command_enum == CommandEnum.PLAY:
            result = self.check_play_card(
                player=player,
                hand_position=hand_position
            )
            if isinstance(result, str):
                return result

            card_list = player.play(hand_position)
            if len(card_list) > 1:
                raise ValueError(f'Mais de uma carta jogada. {card_list}.')

            card: ScoundrelCard = card_list[0]

            if self.game_over:
                action = 'Ganhou o jogo.' if self.hp > 0 else 'Foi derrotado.'
                return self.add_log(action=action, player=player)

            if card.is_weapon is True:
                self.clean_field()
                self.put_in_field(card)
            elif card.is_potion is True:
                self.discard(card)
                if self.healed_this_turn is False:
                    value = card.value
                    return self.heal_hp(value)
                else:
                    action = 'HP já foi curado nesta sala.'
                    return self.add_log(action=action, player=False)
            elif card.is_enemy is True:
                enemy_power = card.value
                player_power = self.power
                damage_value = enemy_power - player_power
                if player_power >= enemy_power:
                    action = f'Ataque contra {card} foi bem sucedido.'
                    self.add_log(action=action, player=player)
                if damage_value > 0:
                    return self.damage_hp(damage_value)

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
    def field_pile(self) -> ScoundrelDeck:
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
        for card in reversed(self.field_pile):
            if card.suit == RoyalSuits.DIAMONDS:
                power = card.value
            elif card.suit in (RoyalSuits.CLUBS, RoyalSuits.SPADES):
                if card.value > power:
                    power = 0

        return power
