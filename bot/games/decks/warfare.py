from operator import attrgetter

from bot.games.decks.deck import BaseDeck
from bot.games.enums.warfare import SymbolsSuits, TerritoryNames


class TerritoriesDeck(BaseDeck):
    def __init__(self, is_shuffle: bool = True, total_decks: int = 1):
        symbols_str_list = SymbolsSuits._member_names_
        symbol_length = len(symbols_str_list)
        quantities = {suit: 0 for suit in SymbolsSuits}
        key = attrgetter("name")
        for i, name_enum in enumerate(sorted(TerritoryNames, key=key)):
            symbol_key = symbols_str_list[i % symbol_length]
            symbol_enum = SymbolsSuits[symbol_key]
            quantities[(name_enum, symbol_enum)] = 1

        super().__init__(
            names=TerritoryNames,
            suits=SymbolsSuits,
            quantities=quantities,
            is_shuffle=is_shuffle,
            total_decks=total_decks,
        )


if __name__ == "__main__":
    deck = TerritoriesDeck(is_shuffle=False, total_decks=1)
    print(len(deck))
    print(deck)
