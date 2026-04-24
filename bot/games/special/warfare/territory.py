import logging

from dataclasses import dataclass, field
from typing import Union

from bot.games.enums.warfare import TerritoryEnum
from bot.games.player import Player


logger = logging.getLogger(__name__)


@dataclass
class Territory:
    name: Union[str, TerritoryEnum]
    occupier: Player = None
    frontiers: "Territory" = field(default_factory=list)
    troops: int = 0

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = TerritoryEnum[self.name]
        if not isinstance(self.name, TerritoryEnum):
            raise TypeError(
                f"O nome do território deve ser do tipo "
                f"str ou TerritoryEnum ({type(self.name)})."
            )

    def add_frontier(self, territory: "Territory"):
        """Adiciona uma fronteira a esse território."""

        error = False
        if not isinstance(territory, Territory):
            tt = type(territory)
            error = True
            logger.warning(f"A fronteira deve ser do tipo Territory ({tt}).")
        if territory is self:
            error = True
            logger.warning(
                f"O território '{territory.name}' não pode ser "
                "fronteira dele mesmo."
            )
            error = True
            logger.warning("Essa fronteira já foi adicionada.")

        if error is False:
            self.frontiers.append(territory)
            if self not in territory.frontiers:
                territory.add_frontier(self)
