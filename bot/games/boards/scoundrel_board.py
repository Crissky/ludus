from typing import List
from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.cards.scoundrel import ScoundrelCard
from bot.games.decks.deck import BaseDeck
from bot.games.decks.scoundrel import ScoundrelDeck
from bot.games.enums.card import RoyalNames, RoyalSuits
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player


class ScoundrelBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = '🦹Scoundrel'
    DESCRIPTION: str = (
        '    SCOUNDREL, um jogo solo de cartas criado por '
        'ZACH GAGE e KURT BIEG.\n\n'

        '✅ RESUMO RÁPIDO:\n'
        f'  {RoyalSuits.CLUBS.value}/{RoyalSuits.SPADES.value} Inimigo: '
        'Encontre ou fuja, vida igual ao valor/poder.\n'
        f'  {RoyalSuits.DIAMONDS.value} Arma: '
        'Equipar, dano recebido reduzido ao atacar.\n'
        f'  {RoyalSuits.HEARTS.value} Poção: '
        'Cura pelo valor/poder da carta, uma por sala.\n'
        '  🫴Passar: Evita sala, cartas para o fundo do deck.\n'
        '  🩸Vida inicial: 20.\n\n'

        '    O baralho padrão não tem os Curingas e nem as seguintes cartas '
        'dos naipes vermelhos '
        f'({RoyalSuits.DIAMONDS.value} e {RoyalSuits.HEARTS.value}): '
        'cartas de figuras '
        f'({RoyalNames.JACK.value}, {RoyalNames.QUEEN.value} e '
        f'{RoyalNames.KING.value}) e nem os Ases ({RoyalNames.ACE.value}) '
        '— total de 44 cartas.\n\n'

        '🎯OBJETIVO:\n'
        '    O jogador começa com 20 pontos de vida (HP) e deve '
        'derrotar todos os Inimigos das Salas das Masmorra. No entanto, '
        'se o HP do jogador chegar a zero, ele perderá a partida.\n\n'

        '🃏TIPOS DE CARTAS:\n'
        f'    As cartas pretas (26 cartas), Espadas {RoyalSuits.SPADES.value} '
        f'e Paus {RoyalSuits.CLUBS.value}, são cartas de Inimigos. Os seus '
        'poderes variam entres 2 e 10 para as cartas de números, '
        f'{RoyalNames.JACK.value}=11, '
        f'{RoyalNames.QUEEN.value}=12, '
        f'{RoyalNames.KING.value}=13 e '
        f'{RoyalNames.ACE.value}=14.\n'
        f'    As cartas de Ouros {RoyalSuits.DIAMONDS.value} (9 cartas) são '
        'Armas. Os seus poderes variam entres 2 e 10 (cartas de números).\n'
        f'    As cartas de Copas {RoyalSuits.HEARTS.value} (9 cartas) são '
        'Poções. Os seus poderes variam entres 2 e 10 (cartas de números).\n\n'

        '🎮ESTRUTURA DO JOGO E RODADAS:\n'
        '    Cada turno começa revelando cartas até formar uma Sala com '
        '4 cartas viradas para cima.\n'
        '    Você pode optar por fugir da sala, devolvendo todas as 4 cartas '
        'para o fundo do baralho. No entanto, não pode fugir duas vezes '
        'seguidas, nem depois de já ter jogado alguma carta na sala atual.\n'
        '    Se permanecer, deve escolher 3 das 4 cartas nessa sala, uma a '
        'uma. A carta restante forma a primeira carta da próxima sala.\n\n'

        '💥AÇÕES DE CADA TIPO DE CARTA:\n'
        f'    Armas ({RoyalSuits.DIAMONDS.value}) — Ao escolher uma Arma, '
        'você a equipa (adiciona ao campo), descartando a anterior e '
        'quaisquer Inimigos que estavam sobre ela. A Arma passa a valer '
        'para combates futuros.\n'
        f'    Poções ({RoyalSuits.HEARTS.value}) — Ao escolher uma Poção, '
        'você bebe e descarta, recuperando vida de acordo com o poder até '
        '20 pontos de vida total. Só pode usar uma por sala; qualquer '
        'outra Poção é descartada sem efeito.\n'
        f'    Inimigos ({RoyalSuits.SPADES.value} e {RoyalSuits.CLUBS.value}) '
        '— ao escolher um Inimigo você o adiciona ao campo. '
        'No entanto, caso o Inimigo tenha poder maior que o poder do Inimigo '
        'mais recente no campo, todas as cartas no campo são descartadas '
        'antes do Inimigo escolhido ser adicionando ao campo. Quando um '
        'Inimigo é adicionado ao campo, um combate é iniciado. Você pode '
        'lutar com as mãos, sofrendo dano igual ao poder do Inimigo, '
        'ou usar a Arma equipada, se disponível. Se usar Arma: subtraia o '
        'valor do poder da Arma do valor do poder do Inimigo; '
        'se o resultado for zero ou menor, você não leva dano. '
        'Se for positivo, leva apenas essa diferença.\n'
        f'    Exemplo: Arma = 5, Inimigo = {RoyalNames.JACK.value}(11): '
        'dano = 11 - 5 = 6.\n'
        '    Após vencer um Inimigo, a Arma só poderá ser usada contra '
        'Inimigos com poder igual ou inferior ao poder do último Inimigo '
        'derrotado.\n\n'

        '🧩 CONDIÇÕES DE VITÓRIA:\n'
        '    O jogo termina se você perder toda a vida (0 HP) (DERROTA) ou se '
        'derrotar todas as cartas de Inimigos da Masmorra (VITÓRIA).'

    )

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = ScoundrelDeck()
        super().__init__(
            draw_pile,
            *players,
            is_shuffle_deck=True,
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
        self.enemy = Player(player_id='0000000000', name='Mestre da Masmorra')
        self.skipped_room = False
        self.is_passing = True
        self.healed_this_turn = False
        self.debug_attr_list.extend([
            'hp',
            'max_hp',
            'enemy',
            'skipped_room',
            'healed_this_turn',
            # 'field_pile',
            'discard_pile',
            'player',
            'power',
        ])

    # SELF METHODS ###########################################################
    def put_in_field(self, *cards: ScoundrelCard) -> str:
        if self.field_pile is None:
            raise ValueError('Campo não existe.')

        pile = self.field_pile
        pile.add(*cards)
        cards_str = ', '.join((card.text for card in cards))
        action = f'Carta(s) adicionada(s) ao campo: {cards_str}.'

        return self.add_log(action=action, player=False)

    def clear_field(self) -> str:
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
        action = f'Perdeu {value} pontos de vida.'

        return self.add_log(action=action, player=False)

    def heal_hp(self, value: int) -> str:
        self.hp += value
        self.hp = min(self.hp, self.max_hp)
        self.healed_this_turn = True
        player = self.player
        action = f'Recuperou {value} pontos de vida.'

        return self.add_log(action=action, player=player)

    def next_turn(self, player: Player, skip: bool = False):
        self.turn += 1
        self.skipped_room = False
        self.is_passing = True
        self.healed_this_turn = False
        if skip is False:
            action = f'Está indo para a Sala {self.turn}.'
        else:
            self.skipped_room = True
            self.is_passing = False
            action = 'Evitou a Sala.'

        self.add_log(action=action, player=player)

    # DRAW METHODS ###########################################################
    def discard(self, *cards: ScoundrelCard) -> str:
        if self.discard_pile is None:
            raise ValueError('Pilha de descarte não existe.')

        pile = self.discard_pile
        pile.add(*cards)
        if cards:
            cards_str = ', '.join((card.text for card in cards))
            action = f'Carta(s) descartada(s): {cards_str}.'
            return self.add_log(action=action, player=False)

    # SHOW BOARD METHODS #####################################################
    def show_board(self, player: Player = None) -> str:
        general_info_list = [self.show_board_field_pile]
        return super().show_board(
            player=player,
            general_info_list=general_info_list
        )

    def show_board_turn(self) -> str:
        return f'HP: {self.hp}/{self.max_hp}\nSala: {self.turn}'

    def show_board_winner(self) -> str:
        winners = self.winners()
        text = None
        if winners:
            text = 'Vencedor: '
            winner = winners[0]
            text += str(winner)

        return text

    def show_board_discard_piles(self) -> str:
        discard_pile = self.discard_pile
        text = discard_pile.peek()[0] if discard_pile else 'Vazia'

        return f'Pilha de Descarte: {text}'

    def show_board_field_pile(self) -> str:
        text = 'Vazio'
        field_pile = self.field_pile
        if field_pile:
            text = ', '.join(c.text for c in reversed(field_pile))

        return f'Campo: {text}'

    # ABSTRACT METHODS #######################################################
    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        keyboard = super().player_keyboard(player=player)
        if isinstance(player, Player) and len(player) > 1:
            for index, button in enumerate(keyboard.play_button_list):
                if button.command == CommandEnum.DRAW:
                    keyboard.play_button_list.pop(index)
                    break

        return keyboard

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
            if len(player) == 1:
                action = 'Não pode jogar com uma carta. Mude de Sala.'
                return self.add_log(action=action, player=False)

            play_card_list = player.play(hand_position)
            if len(play_card_list) > 1:
                player.add_card(*play_card_list)
                raise ValueError(
                    f'Mais de uma carta jogada. {play_card_list}.'
                )

            card: ScoundrelCard = play_card_list[0]
            if card.is_weapon is True:
                self.clear_field()
                self.put_in_field(card)
                weapon_power = card.value
                suit = card.suit.value
                action = (
                    f'Equipou Arma{suit} de {weapon_power} pontos de poder.'
                )
                self.add_log(action=action, player=player)
            elif card.is_potion is True:
                self.discard(card)
                if self.healed_this_turn is False:
                    value = card.value
                    self.heal_hp(value)
                else:
                    action = 'HP já foi curado nesta Sala.'
                    self.add_log(action=action, player=False)
            elif card.is_enemy is True:
                field_pile = self.field_pile
                peeked_list = field_pile.peek()
                last_enemy = peeked_list[0] if peeked_list else None
                if (
                    isinstance(last_enemy, ScoundrelCard)
                    and last_enemy.is_enemy is True
                    and card.value > last_enemy.value
                ):
                    self.clear_field()

                enemy_power = card.value
                player_power = self.power
                damage_value = enemy_power - player_power
                self.put_in_field(card)
                if player_power >= enemy_power:
                    action = f'Derrotou {card} sem receber dano.'
                    self.add_log(action=action, player=player)
                if damage_value > 0:
                    action = f'Derrotou {card}, mas recebeu dano.'
                    self.add_log(action=action, player=player)
                    self.damage_hp(damage_value)

            if len(player) < 4:
                self.is_passing = False
            else:
                self.is_passing = True
        elif command_enum == CommandEnum.DRAW:
            if len(player) > 1:
                action = 'Você só pode passar a Sala com uma carta na mão.'
                return self.add_log(action=action, player=False)

            quantity = player.hand.max_size - len(player)
            card_list = self.draw_pile.draw(quantity=quantity)
            player.hand.add_card(*card_list)
            self.next_turn(player=player, skip=False)
        elif command_enum == CommandEnum.PASS:
            if len(player) != 4:
                action = 'Só pode pular a Sala com 4 cartas na mão.'
                return self.add_log(action=action, player=False)
            if self.skipped_room is True:
                action = 'Não pode passar a Sala duas vezes seguidas.'
                return self.add_log(action=action, player=False)

            quantity = len(player.hand)
            max_size = player.hand.max_size

            discard_list = player.discard(quantity=quantity)
            self.draw_pile.add_bottom(*discard_list)

            card_list = self.draw_pile.draw(quantity=max_size)
            player.hand.add_card(*card_list)
            self.next_turn(player=player, skip=True)

        if self.game_over:
            winners_list = self.winners()
            winner = winners_list[0] if winners_list else None
            player = self.player
            if winner is None:
                action = 'Empate.'
            elif winner == self.enemy:
                action = 'Foi derrotado!'
                if self.hp <= 0:
                    action += ' HP zerado.'
                elif self.can_play is False:
                    action += ' Não há mais jogadas válidas.'
            elif winner == player and player is not None:
                action = f'Parabens, {player.name}! Você ganhou o jogo!!!'

            return self.add_log(action=action, player=player)

    def is_playable_card(self, card: ScoundrelCard) -> bool:
        player = self.player

        if isinstance(player, Player) and len(player) == 1:
            return False
        elif not isinstance(card, ScoundrelCard):
            return False
        else:
            return True

    def winners(self) -> List[Player]:
        winners = []
        player = self.player

        if self.is_started is False:
            winners = []
        elif player is None:
            winners = []
        elif (
            self.hp > 0 and
            self.draw_pile.is_empty is True and
            self.enemy_in_room is False
        ):
            winners = self.player_list.copy()
        elif self.hp <= 0:
            winners = [self.enemy]
        elif self.can_play is False:
            winners = [self.enemy]

        return winners

    # PROPERTIES METHODS #####################################################
    @property
    def field_pile(self) -> BaseDeck:
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

    @property
    def player(self) -> Player:
        return self.player_list[0] if self.player_list else None

    @property
    def power(self) -> int:
        power = 0
        for card in reversed(self.field_pile):
            if card.suit == RoyalSuits.DIAMONDS:
                power = card.value
            # elif card.suit in (RoyalSuits.CLUBS, RoyalSuits.SPADES):
            #     if card.value > power:
            #         power = 0

        return power

    @property
    def enemy_in_room(self) -> bool:
        player = self.player
        if isinstance(player, Player):
            card_list: List[ScoundrelCard] = list(player)
            for card in card_list:
                if card.is_enemy is True:
                    return True

        return False

    @property
    def can_play(self) -> bool:
        player = self.player
        if player is None:
            return False

        total_cards = len(player)
        playable_card = any((self.is_playable_card(c) for c in player))

        if total_cards == 1:
            return True
        elif total_cards == 4 and self.skipped_room is False:
            return True
        elif total_cards > 1 and playable_card is True:
            return True
        else:
            return False
