
from dataclasses import dataclass, field
from typing import Union

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.player import Player


logger = logging.getLogger(__name__)


@dataclass
class Territory:
    name: Union[str, TerritoryEnum]
    occupier: Player = None
    frontiers: "Territory" = field(default_factory=list)
    troops: int = 0


@dataclass
class Continent:
    name: Union[str, ContinentEnum]
    majority_bonus: int
    totality_bonus: int
    territories: list = field(default_factory=list)

    def __post_init__(self):
        if self.totality_bonus <= self.majority_bonus:
            raise ValueError(
                "O bônus pela dominância total deve ser maior que o bônus "
                "pela maioria dos territórios.\n"
                f"BÔNUS DE MAIORIA: {self.majority_bonus}.\n"
                f"BÔNUS TOTAL: {self.totality_bonus}."
            )
        if self.majority_bonus == 0 or self.totality_bonus == 0:
            majority_text = ""
            totality_text = ""
            if self.majority_bonus == 0:
                majority_text = f"BÔNUS DE MAIORIA: {self.majority_bonus}.\n"
            if self.totality_bonus == 0:
                totality_text = f"BÔNUS TOTAL: {self.totality_bonus}."

            raise ValueError(
                "Os bônus devem ser maiores que zero.\n{}{}".format(
                    majority_text, totality_text
                )
            )

    def __iter__(self):
        yield from self.territories


@dataclass
class World:
    continents: list = field(default_factory=list)

    def __post_init__(self):
        self.territories = []
        for cont in self.continents:
            self.territories.extend(cont.territories)
