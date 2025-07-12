from typing import List
from bot.games.boards.cardgame_board import BaseCardGameBoard
from bot.games.buttons.play_button import PlayButton
from bot.games.cards.card import Card
from bot.games.decks.color import ColorDeck
from bot.games.enums.card import WILD_SUITS, ColorNames, ColorSuits
from bot.games.enums.command import CallbackKeyEnum, CommandEnum
from bot.games.play_keyboard import PlayKeyBoard
from bot.games.player import Player


class ColorsGameBoard(BaseCardGameBoard):
    DISPLAY_NAME: str = 'Colors'
    DESCRIPTION: str = None

    def __init__(self, *players: Player):
        draw_pile = ColorDeck(shuffle=False)
        super().__init__(
            draw_pile,
            *players,
            total_discard_pile=1,
            initial_hand_size=7,
            hand_kwargs={},
            min_total_players=2,
            max_total_players=4,
        )
        self.pending_draw = 0
        self.selecting_color = False

    def player_keyboard(self, player: Player) -> PlayKeyBoard:
        if all((
            self.selecting_color is True,
            self.is_started is True,
            player == self.current_player,
            not self.game_over
        )):
            keyboard = PlayKeyBoard(buttons_per_row=self.initial_hand_size)

            for color_suit in ColorSuits:
                if color_suit not in WILD_SUITS:
                    text = color_suit.value
                    callback_data_args = {
                        CallbackKeyEnum.SELECTED_COLOR.name: color_suit.name,
                    }
                    button = PlayButton(
                        text=text,
                        game=self,
                        command=CommandEnum.SELECT_COLOR,
                        **callback_data_args
                    )
                    keyboard.add_button(button)

            return keyboard
        else:
            return super().player_keyboard(player)

    def play(self, player: Player, play_dict: dict):
        command_str = play_dict[CallbackKeyEnum.COMMAND]
        command_enum = CommandEnum[command_str]
        game_id = play_dict[CallbackKeyEnum.GAME_ID]
        hand_position = play_dict.get(CallbackKeyEnum.HAND_POSITION)
        selected_color_str = play_dict.get(CallbackKeyEnum.SELECTED_COLOR)

        if game_id != self.id:
            action = f'Jogo inválido: {game_id}'
            return self.add_log(player=False, action=action)
        if player != self.current_player:
            action = f'Não é a vez de {player}.'
            return self.add_log(player=False, action=action)
        if not self.player_in_game(player):
            action = f'{player} não está mais na partida.'
            return self.add_log(player=False, action=action)

        player = self.get_player(player)

        if command_enum == CommandEnum.PLAY:
            card_list = player.peek(hand_position)
            card = card_list[0]
            if not isinstance(card, Card):
                action = f'Carta na posição {hand_position} não encontrada.'
                return self.add_log(player=player, action=action)
            if not self.is_playable_card(card=card):
                action = f'Carta {card} não pode ser jogada.'
                return self.add_log(player=player, action=action)

            self.is_passing = False
            card_list = player.play(hand_position)
            card = card_list[0]
            self.discard(card)
            action = f'jogou {card}.'
            self.add_log(player=player, action=action)

            if card.plus_value > 0:
                self.pending_draw += card.plus_value
            elif card.name == ColorNames.BLOCK:
                self.next_turn(skip=True)
                action = 'Bloqueou o próximo jogador.'
                self.add_log(player=player, action=action)
            elif card.name == ColorNames.REVERSE:
                self.invert_direction()
                if len(self.player_list) == 2:
                    self.next_turn(skip=True)
                    action = 'Bloqueou o próximo jogador.'
                    self.add_log(player=player, action=action)
                else:
                    action = f'Inverteu{ColorNames.REVERSE.value} o jogo.'
                    self.add_log(player=player, action=action)

            if card.is_wild:
                self.selecting_color = True

            if (
                card.name not in [ColorNames.BLOCK, ColorNames.REVERSE]
                and not card.is_wild
            ):
                self.next_turn(skip=False)
                action = 'Passou a vez.'
                self.add_log(player=player, action=action)

        elif command_enum == CommandEnum.DRAW:
            draw_quantity = max(1, self.pending_draw)
            card_list = self.draw(quantity=draw_quantity)
            discarded_card_list = player.add_card(*card_list)
            self.discard(*discarded_card_list)

            action = f'Comprou {draw_quantity} carta(s).'
            self.add_log(player=player, action=action)

            self.is_passing = True
            if self.pending_draw > 0:
                self.pending_draw = 0
                self.is_passing = False
                self.next_turn(skip=False)
                action = 'Passou a vez.'
                self.add_log(player=player, action=action)

        elif command_enum == CommandEnum.PASS:
            self.is_passing = False
            self.next_turn(skip=False)
            action = 'Passou a vez.'
            self.add_log(player=player, action=action)
        elif command_enum == CommandEnum.SELECT_COLOR:
            color_suit_enum = ColorSuits[selected_color_str]
            discard_pile = self.discard_piles[0]
            peeked_card_list = discard_pile.peek()
            top_card = peeked_card_list[0]
            top_card.set_wild_suit(suit=color_suit_enum)
            self.selecting_color = False
            self.next_turn(skip=False)
            action = 'Passou a vez.'
            self.add_log(player=player, action=action)

    def is_playable_card(self, card: Card) -> bool:
        for discard_pile in self.discard_piles:
            if not discard_pile:
                return True

            peeked_card_list = discard_pile.peek()
            top_card = peeked_card_list[0]

            # Testa o empilhamento de carta PLUS
            if self.pending_draw > 0:
                if (
                    card.plus_value > 0 and
                    card.plus_value >= top_card.plus_value
                ):
                    return True
                return False

            # Caso normal: tem que bater cor ou nome
            if (
                card.suit == top_card.suit or
                card.name == top_card.name or
                card.is_wild
            ):
                return True

        return False

    def winners(self) -> List[Player]:
        return [
            player
            for player in self.player_list
            if len(player.hand) == 0 and self.is_started is True
        ]
