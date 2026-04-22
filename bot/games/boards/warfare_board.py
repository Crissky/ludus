
from dataclasses import dataclass, field
import logging
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

    def add_frontier(self, territory: "Territory"):
        """Adiciona uma fronteira a esse território."""

        error = False
        if not isinstance(territory, Territory):
            tt = type(territory)
            error = True
            logger.warning(f"A fronteira deve ser do tipo Territory ({tt}).")
        if territory is self:
            error = True
            logger.warning("O território não pode ser fronteira dele mesmo.")
        if territory in self.frontiers:
            error = True
            logger.warning("Essa fronteira já foi adicionada.")

        if error is False:
            self.frontiers.append(territory)
            if self not in territory.frontiers:
                territory.add_frontier(self)


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
