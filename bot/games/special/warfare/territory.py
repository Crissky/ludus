import logging

from dataclasses import dataclass, field
from typing import Dict, List, Union

from bot.games.enums.warfare import TerritoryEnum
from bot.games.player import Player


logger = logging.getLogger(__name__)


@dataclass
class Territory:
    name: Union[str, TerritoryEnum]
    occupier: Player = None
    frontiers: Dict[TerritoryEnum, "Territory"] = field(default_factory=dict)
    troops: int = 0

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = TerritoryEnum[self.name]
        if not isinstance(self.name, TerritoryEnum):
            raise TypeError(
                f"O nome do território deve ser do tipo "
                f"str ou TerritoryEnum ({type(self.name)})."
            )

    def __getitem__(self, key) -> "Territory":
        return self.frontiers[key]

    def add_frontier(self, territory: "Territory"):
        """Adiciona uma fronteira a esse território."""

        error = False
        if not isinstance(territory, Territory):
            tt = type(territory)
            raise TypeError(f"A fronteira deve ser do tipo Territory ({tt}).")
        if territory is self:
            error = True
            logger.warning(
                f"O território '{territory.show_name}' não pode ser "
                "fronteira dele mesmo."
            )
        if territory in self.frontier_territories:
            error = True
            logger.warning(
                f"O território '{territory.show_name}' já é fronteira do "
                f"território '{self.show_name}'."
            )

        if error is False:
            self.frontiers[territory.name] = territory
            if self not in territory.frontier_territories:
                territory.add_frontier(self)

    @property
    def min_troops_on_conquest(self):
        return 1

    @property
    def max_troops_on_conquest(self):
        return 3

    @property
    def frontier_territories(self) -> List["Territory"]:
        return list(self.frontiers.values())

    @property
    def show_name(self) -> str:
        return self.name.name

    @property
    def show_value(self) -> str:
        return self.name.value

    @property
    def format_name(self) -> str:
        return f"território '{self.show_name}'"

    @property
    def occupier_name(self) -> str:
        return "SEM OCUPANTE" if self.occupier is None else self.occupier.name
