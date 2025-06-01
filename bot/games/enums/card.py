from enum import Enum


# Suits
class RoyalSuits(Enum):
    CLUBS = "♣️"
    DIAMONDS = "♦️"
    HEARTS = "♥️"
    SPADES = "♠️"


class SpanishSuits(Enum):
    CLUBS = "🦯"
    COINS = "🪙"
    CUPS = "🍷"
    SWORDS = "⚔️"


class ColorSuits(Enum):
    RED = "🔴"
    BLUE = "🔵"
    GREEN = "🟢"
    YELLOW = "🟡"
    BLACK = "⚫️"


class ElementalSuits(Enum):
    FIRE = "🔥"
    WATER = "🌊"
    EARTH = "🌳"
    SKY = "☀️"
    VOID = "🌑"


# Names
class RoyalNames(Enum):
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


class SpanishNames(Enum):
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


class StrippedSpanishNames(Enum):
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
