from collections.abc import Generator
from itertools import product
from typing import List, Type, Union

from bot.games.cards.card import Card
from bot.games.enums.card import Names, Suits
from bot.games.structure.stack import Stack


class BaseDeck:
    def __init__(
        self,
        names: Type[Names] = None,
        suits: Type[Suits] = None,
        quantities: dict = None,
        is_shuffle: bool = True,
        total_decks: int = 1,
        card_class: Type[Card] = Card
    ):
        """Se names ou suits for None, o deck será vazio.

        As cartas são geradas de acordo com o dicionário quantity
        Caso seja igual a None, Será gerado uma carta para o produto de
        Suits x Names.

        Caso o dicionário seja definido, as quantidade serão definidas
        obedecendo as seguintes prioridades de acordo com o tipo de chave:
            1. (Name, Suit): Define a quantidade de carta para determinado
                Name e Suit.
            2. Name: Define a quantidade de cartas de determinado Name,
                exceto as que foram definidas no (Name, Suit).
            3. Suit: Define a quantidade de cartas de determinado Suit,
                exceto as que foram definidas no (Name, Suit) e Name.

        Exemplo: quantity = {
            (ColorNames.ZERO, ColorSuits.BLACK): 0,
            ColorNames.ZERO: 1,
            ColorSuits.BLACK: 2,
        }
        - Não havera cartas BLACK e ZERO.
        - Haverá 1 carta ZERO de todas as cores (Suits), exceto BLACK.
        - Haverá 2 cartas BLACK de todos os valores (Names), exceto ZERO.
        """

        self.names = names
        self.suits = suits
        self.quantities = quantities
        self.is_shuffle = is_shuffle
        self.total_decks = total_decks
        self.card_class = card_class
        self.card_stack = Stack()
        if (
            quantities is None and
            suits is not None and
            issubclass(suits, Suits)
        ):
            quantities = {suit: 1 for suit in suits}

        if names is None or suits is None:
            names_suits = []
        elif issubclass(names, Names) and issubclass(suits, Suits):
            names_suits = product(names, suits)
        else:
            raise TypeError(
                f'Combinação inválida de '
                f'names ({type(names)}) e suits ({type(suits)}). '
                'names precisa ser um subclasse de Names e '
                'suits precisa ser um subclasse de Suits '
                'ou ambos None.'
            )

        if not isinstance(is_shuffle, bool):
            raise TypeError(
                f'is_shuffle precisa ser um booleano, não {type(is_shuffle)}.'
            )

        if not isinstance(quantities, dict) and quantities is not None:
            raise TypeError(
                f'quantities precisa ser um dicionário ou None, '
                f'não {type(quantities)}.'
            )

        if not isinstance(total_decks, int):
            raise TypeError(
                f'total_decks precisa ser um inteiro, não {type(total_decks)}.'
            )
        elif total_decks < 1:
            raise ValueError(
                f'total_decks precisa ser maior que 0, não {total_decks}.'
            )

        if not issubclass(card_class, Card):
            raise TypeError(
                f'card_class precisa ser um subclasse de Card, '
                f'não {type(card_class)}.'
            )

        for name, suit in names_suits:
            name_suit_qty = quantities.get((name, suit))
            name_qty = quantities.get(name)
            suit_qty = quantities.get(suit, 1)
            if isinstance(name_suit_qty, int):
                card_qty = name_suit_qty
            elif isinstance(name_qty, int):
                card_qty = name_qty
            else:
                card_qty = suit_qty
            for _ in range(card_qty * total_decks):
                self.card_stack.push(card_class(name=name, suit=suit))

        if is_shuffle is True:
            self.shuffle()

    def __bool__(self) -> bool:
        return bool(self.card_stack)

    def __iter__(self) -> Generator[Card]:
        return iter(self.card_stack)

    def __len__(self) -> int:
        return len(self.card_stack)

    def __getitem__(self, index) -> Union[Card, List[Card]]:
        return self.card_stack[index]

    def __str__(self) -> str:
        return self.card_stack.text_horizontal

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.card_stack.text_horizontal})'

    def draw(self, quantity: int = 1) -> List[Card]:
        card_list = self.card_stack.pop(quantity=quantity)
        card_list = self.make_card_list(card_list=card_list)

        return card_list

    def peek(self, quantity: int = 1) -> List[Card]:
        card_list = self.card_stack.peek(quantity=quantity)
        card_list = self.make_card_list(card_list=card_list)

        return card_list

    def peek_bottom(self, quantity: int = 1) -> List[Card]:
        card_list = self.card_stack.peek_bottom(quantity=quantity)
        card_list = self.make_card_list(card_list=card_list)

        return card_list

    def add(self, *cards: Card):
        self.card_stack.push(*cards)

    def add_bottom(self, *cards: Card):
        self.card_stack.push_bottom(*cards)

    def shuffle(self):
        self.card_stack.shuffle()

    def make_card_list(self, card_list: List[Card]) -> List[Card]:
        if isinstance(card_list, Card):
            card_list = [card_list]
        if card_list is None:
            card_list = []

        return card_list

    @property
    def is_empty(self) -> bool:
        return self.card_stack.is_empty
