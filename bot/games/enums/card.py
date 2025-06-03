from enum import Enum


class Suits(Enum):
    ...


class Names(Enum):
    ...

# Suits


class RoyalSuits(Suits):
    CLUBS = "♣️"
    DIAMONDS = "♦️"
    HEARTS = "♥️"
    SPADES = "♠️"


class SpanishSuits(Suits):
    CLUBS = "🦯"
    COINS = "🪙"
    CUPS = "🍷"
    SWORDS = "⚔️"


class ColorSuits(Suits):
    RED = "🔴"
    BLUE = "🔵"
    GREEN = "🟢"
    YELLOW = "🟡"
    BLACK = "⬛"


class ElementalSuits(Suits):
    FIRE = "🔥"
    WATER = "🌊"
    EARTH = "🌳"
    SKY = "☀️"
    VOID = "🌑"


# Names
class RoyalNames(Names):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


class ColorNames(Names):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    BLOCK = "⊘"
    REVERSE = "🗘"  # "🌀"
    PLUS_ZERO = ""
    PLUS_TWO = "+2"
    PLUS_FOUR = "+4"


class SpanishNames(Names):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    KNAVE = "10"
    KNIGHT = "11"
    KING = "12"


class StrippedSpanishNames(Names):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    KNAVE = "10"
    KNIGHT = "11"
    KING = "12"
