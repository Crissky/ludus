from bot.games.decks.deck import BaseDeck
from bot.games.enums.card import RoyalNames, RoyalSuits


class RoyalDeck(BaseDeck):
    def __init__(self, shuffle=True):
        super().__init__(names=RoyalNames, suits=RoyalSuits, shuffle=shuffle)


if __name__ == '__main__':
    deck = RoyalDeck(shuffle=False)
    print(len(deck))
    print(deck)
