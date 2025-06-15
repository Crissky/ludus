import re
from bot.games.cards.card import Card
from bot.games.enums.card import Names, Suits


class FlipCard(Card):
    def __init__(
        self,
        name: Names,
        suit: Suits,
        flip_name: Names,
        flip_suit: Suits
    ):
        super().__init__(name, suit)
        if not isinstance(flip_name, Names):
            raise TypeError('flip_name precisa ser um Enum do tipo Names.')
        if not isinstance(flip_suit, Suits):
            raise TypeError('flip_suit precisa ser um Enum do tipo Suits.')

        self.flip_name = flip_name
        self.flip_suit = flip_suit
        self.flip_wild_name = None
        self.flip_wild_suit = None
        self.is_flipped = False

    def flip(self):
        self.is_flipped = not self.is_flipped

    def set_wild_name(self, name: Names):
        if not re.search(self.wild_terms, self.suit.name, re.I):
            raise ValueError(f'{self.suit.name} não é um valor WILD válido.')
        if not isinstance(name, self.name.__class__):
            raise TypeError(
                f'name precisa ser um Enum do tipo {self.name.__class__}.'
            )

        if self.is_flipped is True:
            self.flip_wild_name = name
        else:
            self.wild_name = name

    def set_wild_suit(self, suit: Suits):
        if not re.search(self.wild_terms, self.suit.name, re.I):
            raise ValueError(f'{self.suit.name} não é um valor WILD válido.')
        if not isinstance(suit, self.suit.__class__):
            raise TypeError(
                f'suit precisa ser um Enum do tipo {self.suit.__class__}.'
            )

        if self.is_flipped is True:
            self.flip_wild_suit = suit
        else:
            self.wild_suit = suit

    def unset_wild(self):
        self.wild_name = None
        self.wild_suit = None
        self.flip_wild_name = None
        self.flip_wild_suit = None

    def get_name(self) -> Names:
        return (
            self.wild_name
            if self.wild_name is not None
            else self.real_name
        )

    def get_flip_name(self) -> Names:
        return (
            self.flip_wild_name
            if self.flip_wild_name is not None
            else self.flip_name
        )

    def get_suit(self) -> Suits:
        return (
            self.wild_suit
            if self.wild_suit is not None
            else self.real_suit
        )

    def get_flip_suit(self) -> Suits:
        return (
            self.flip_wild_suit
            if self.flip_wild_suit is not None
            else self.flip_suit
        )

    @property
    def full_text(self):
        name = self.get_name().value
        suit = self.get_suit().value
        flip_name = self.get_flip_name().value
        flip_suit = self.get_flip_suit().value
        return f'{suit}{name} | {flip_suit}{flip_name}'

    @property
    def name(self):
        if self.is_flipped is True:
            return self.get_flip_name()
        else:
            return self.get_name()

    @property
    def suit(self):
        if self.is_flipped is True:
            return self.get_flip_suit()
        else:
            return self.get_suit()


if __name__ == '__main__':
    from bot.games.enums.card import (
        ColorNames, ColorSuits, FlipColorNames, FlipColorSuits
    )
    card = FlipCard(
        name=ColorNames.PLUS_FOUR,
        suit=ColorSuits.RED,
        flip_name=FlipColorNames.PLUS_FIVE,
        flip_suit=FlipColorSuits.ORAGE
    )
    print(card.full_text)
    print(card.name)
    print(card.suit)
    print(card.value)
    print(card.text)
    card.flip()
    print(card.full_text)
    print(card.name)
    print(card.suit)
    print(card.value)
    print(card.text)
