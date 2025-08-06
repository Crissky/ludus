from typing import List
from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.deck import BaseDeck
from bot.games.decks.royal import RoyalDeck
from bot.games.enums.card import FullRoyalNames, FullRoyalSuits
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player


class JokerJailBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = 'Joker Jail'
    DESCRIPTION: str = (
        'DESCRIÇÃO E REGRAS DO JOKER JAIL PRECISAM SER DEFINIDAS.'
    )

    def __init__(self, *players: Player, debug: bool = False):
        draw_pile = RoyalDeck(is_shuffle=True)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=9,
            discard_at_start=True,
            initial_hand_size=0,
            hand_kwargs={'max_size': 0},
            min_total_players=1,
            max_total_players=1,
            debug=debug,
        )
        self.joker_card = Card(
            name=FullRoyalNames.JOKER,
            suit=FullRoyalSuits.JOKER
        )
        self.wall_indexes = [1, 3, 5, 7]
        self.corner_indexes = [0, 2, 6, 8]
        self.joker_indexes = [4]
        self.selected_card_indexes = []
        self.enemy = Player(player_id='0000000000', name='Carcereiro')

        self.debug_attr_list.extend([
            'joker_card',
            'wall_indexes',
            'corner_indexes',
            'joker_indexes',
            'selected_card_indexes',
        ])

    def sum_card_values(self) -> dict:
        black_cards: List[Card] = []
        red_cards: List[Card] = []
        for index in set(self.selected_card_indexes):
            pile: BaseDeck = self.discard_piles[index]
            if pile.is_empty is True:
                raise ValueError(f'Pilha {index} não possui carta.')
            card = pile.peek(quantity=1)[0]
            if card.is_black is True:
                black_cards.append(card)
            elif card.is_red is True:
                red_cards.append(card)
            else:
                raise ValueError(f'Carta {card} não é preta ou vermelha.')

        if not black_cards:
            raise ValueError('Não há cartas pretas selecionadas.')
        if not red_cards:
            raise ValueError('Não há cartas vermelhas selecionadas.')

        black_value = sum(((card.value+1) for card in black_cards))
        red_value = sum(((card.value+1) for card in red_cards))

        return {'black': black_value, 'red': red_value}

    def drop_selected_cards(self) -> List[Card]:
        card_list = []
        for index in self.selected_card_indexes:
            discard_pile: BaseDeck = self.discard_piles[index]
            card = discard_pile.draw(quantity=1)[0] if discard_pile else None
            if card:
                card_list.append(card)

        return card_list

    def create_discard_pile(self):
        self.discard_piles = [
            BaseDeck()
            for _ in range(self.total_discard_pile)
        ]

        for _ in range(6):
            for index in self.wall_indexes:
                wall_pile = self.discard_piles[index]
                cards = self.draw()
                wall_pile.add(*cards)

        for _ in range(2):
            for index in self.corner_indexes:
                corner_pile = self.discard_piles[index]
                cards = self.draw()
                corner_pile.add(*cards)

        joker_pile = self.joker_pile
        joker_pile.add(self.joker_card)

    def show_board(self, player: Player = None) -> str:
        general_info_list = [self.show_selected_cards]
        return super().show_board(
            player=player,
            general_info_list=general_info_list
        )

    def show_board_discard_piles(self) -> str:
        text_list = []
        peek_discard_piles = ''
        for discard_pile in self.discard_piles:
            text = str(len(discard_pile)) if discard_pile else '🚫'
            text = text.zfill(2)
            text_list.append(text)

        for index in range(0, len(text_list), 3):
            peek_discard_piles += '|'.join(text_list[index:index + 3]) + '\n'

        return f'Pilha de Descarte:\n{peek_discard_piles[:-1]}'

    def show_selected_cards(self) -> str:
        selected_card_list = []
        for index in self.selected_card_indexes:
            discard_pile: BaseDeck = self.discard_piles[index]
            if discard_pile:
                card = discard_pile.peek(quantity=1)[0]
                selected_card_list.append(card)

        selected_cards = ', '.join((str(card) for card in selected_card_list))
        if not selected_cards:
            return None

        return f'Cartas selecionadas: {selected_cards}'

    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if self.is_started is not True:
            return self.invite_keyboard

        keyboard = PlayKeyBoard(buttons_per_row=3)
        if player != self.current_player:
            return keyboard
        if self.game_over:
            return keyboard

        for index, pile in enumerate(self.discard_piles):
            card = None
            if pile:
                card = pile.peek(quantity=1)[0]

            text = card.text if card else '❌'
            callback_data_args = {CallbackKeyEnum.DISCARD_POSITION.name: index}
            button = PlayButton(
                text=text,
                game=self,
                command=CommandEnum.PLAY,
                **callback_data_args

            )
            keyboard.add_button(button)

        if self.is_passing is True:
            button = self.pass_button
        else:
            button = self.draw_button
        keyboard.add_button(button)

        if len(self.selected_card_indexes) >= 2:
            button = self.calculate_button
            keyboard.add_button(button)

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
        discard_position = play_dict.get(CallbackKeyEnum.DISCARD_POSITION)

        if command_enum == CommandEnum.PLAY:
            if discard_position >= len(self.discard_piles):
                action = f'Pilha número {discard_position+1} não existe.'
                return self.add_log(action=action, player=False)

            discard_pile: BaseDeck = self.discard_piles[discard_position]
            card_list = discard_pile.peek(quantity=1)
            card = card_list[0] if card_list else None

            if discard_position in self.selected_card_indexes:
                self.selected_card_indexes.remove(discard_position)
                action = f'Carta {card} foi desselecionada.'
                return self.add_log(action=action, player=False)
            elif discard_pile.is_empty is True:
                action = f'Pilha número {discard_position+1} está vazia.'
                return self.add_log(action=action, player=False)
            elif (
                discard_position in self.wall_indexes
                or discard_position in self.corner_indexes
                or (
                    discard_position in self.joker_indexes
                    and self.joker_in_top is False
                )
            ):
                self.selected_card_indexes.append(discard_position)
                action = f'Carta {card} foi selecionada.'
                self.add_log(action=action, player=False)
                return None
            elif (
                discard_position in self.joker_indexes
                and self.joker_in_top is True
            ):
                action = f'Carta JOKER {card} não pode ser selecionada.'
                return self.add_log(action=action, player=False)
            else:
                action = (
                    f'ERRO: Jogada não computada para a carta "{card}" '
                    f'(discard_position={discard_position}).'
                )
                return self.add_log(action=action, player=False)

        elif command_enum == CommandEnum.DRAW:
            card_list = self.draw_pile.draw(quantity=1)
            card = card_list[0] if card_list else None
            if card is None:
                action = 'Não há mais cartas para comprar.'
                return self.add_log(action=action, player=False)
            else:
                joker_index = self.joker_indexes[0]
                joker_pile = self.discard_piles[joker_index]
                joker_pile.add(card)
                action = f'Carta {card} adicionada ao topo da Pilha Central.'
                return self.add_log(action=action, player=False)
        elif command_enum == CommandEnum.CALCULATE:
            ...

    def is_playable_card(self, card: Card) -> bool:
        return True

    def winners(self) -> List[Player]:
        winners = []
        if self.is_started is True:
            for index in self.wall_indexes:
                pile = self.discard_piles[index]
                if pile.is_empty is True and self.joker_in_top is True:
                    player = self.player
                    winners.append(player)
                    break

        return winners

    @property
    def player(self) -> Player:
        return self.player_list[0] if self.player_list else None

    @property
    def joker_pile(self) -> BaseDeck:
        joker_index = self.joker_indexes[0]
        joker_pile = self.discard_piles[joker_index]

        return joker_pile

    @property
    def joker_in_top(self) -> bool:
        joker_pile = self.joker_pile
        if joker_pile.is_empty:
            return False

        top_card = joker_pile.peek(quantity=1)[0]
        return top_card == self.joker_card

    @property
    def has_select_black(self) -> bool:
        for index in self.selected_card_indexes:
            pile: BaseDeck = self.discard_piles[index]
            if pile.is_empty is True:
                continue

            card = pile.peek(quantity=1)[0]
            if card.is_black is True:
                return True

        return False

    @property
    def has_select_red(self) -> bool:
        for index in self.selected_card_indexes:
            pile: BaseDeck = self.discard_piles[index]
            if pile.is_empty is True:
                continue

            card = pile.peek(quantity=1)[0]
            if card.is_red is True:
                return True

        return False

    @property
    def calculate_button(self) -> PlayButton:
        return PlayButton(
            text='Calcular🔢',
            game=self,
            command=CommandEnum.CALCULATE,
            group=2
        )
