import logging

from dataclasses import dataclass, field
from typing import Dict, List, Union

from bot.games.enums.warfare import TerritoryEnum
from bot.games.player import Player


logger = logging.getLogger(__name__)


@dataclass
class Territory:
    name: Union[str, TerritoryEnum]
    color_emoji: str = None
    occupier: Player = None
    frontiers: Dict[TerritoryEnum, "Territory"] = field(
        default_factory=dict, repr=False
    )
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
                f"O {territory.format_name} não pode ser fronteira dele mesmo."
            )
        if territory in self.frontier_territories:
            error = True
            logger.warning(
                f"O {self.show_name} já é fronteira do "
                f"{territory.format_name}."
            )

        if error is False:
            self.frontiers[territory.name] = territory
            logger.info(
                f"O {territory.format_name} foi adicionado a fronteira do "
                f"{self.format_name}."
            )
            if self not in territory.frontier_territories:
                territory.add_frontier(self)

    def add_occupier(self, player: Player, troops: int):
        """Adiciona um jogador ao território"""
        if self.occupier is not None:
            raise ValueError(
                f"O {self.format_name} já possui um ocupante "
                f"({self.occupier_name})."
            )
        if troops != self.min_troops_on_conquest:
            raise ValueError(
                f"O número de tropas ({troops}) para adicionar no "
                f"{self.format_name} é diferente do permitido "
                f"({self.min_troops_on_conquest})."
            )

        self.occupier = player
        self.troops = troops
        logger.info(
            f"O {player.format_name} foi adicionado ao {self.format_name}."
        )

    def change_occupier(self, player: Player, troops: int):
        """Altera o ocupante do território"""

        if player is self.occupier:
            raise ValueError(
                f"O {player.format_name} já é ocupante do {self.format_name}."
            )
        if troops < self.min_troops_on_conquest:
            raise ValueError(
                f"O número de tropas ({troops}) para para conquistar o "
                f"{self.format_name} é menor que o permitido "
                f"({self.min_troops_on_conquest})."
            )
        if troops > self.max_troops_on_conquest:
            raise ValueError(
                f"O número de tropas ({troops}) para para conquistar o "
                f"{self.format_name} é maior que o permitido "
                f"({self.max_troops_on_conquest})."
            )

        self.occupier = player
        self.troops = troops
        logger.info(
            f"O {player.format_name} conquistou o {self.format_name} com "
            f"{troops} tropas."
        )

    conquer_territory = change_occupier

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
        color_emoji = "" if self.color_emoji is None else self.color_emoji
        return color_emoji + self.name.name

    @property
    def show_value(self) -> str:
        color_emoji = "" if self.color_emoji is None else self.color_emoji
        return color_emoji + self.name.value

    @property
    def format_name(self) -> str:
        return f"território '{self.show_name}'"

    @property
    def occupier_name(self) -> str:
        return "SEM OCUPANTE" if self.occupier is None else self.occupier.name
