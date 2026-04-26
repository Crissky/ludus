import logging

from dataclasses import dataclass, field
from typing import Dict, List, Union

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.special.warfare.territory import Territory


logger = logging.getLogger(__name__)


@dataclass
class Continent:
    name: Union[str, ContinentEnum]
    color_emoji: str
    totality_bonus: int
    majority_bonus: int = 0
    territories: Dict[TerritoryEnum, Territory] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = ContinentEnum[self.name]
        if not isinstance(self.name, ContinentEnum):
            raise TypeError(
                f"O nome do continente deve ser do tipo "
                f"str ou ContinentEnum ({type(self.name)})."
            )

        if self.totality_bonus < self.majority_bonus:
            raise ValueError(
                "O bônus pela dominância total deve ser igual ou maior que "
                "o bônus pela maioria dos territórios.\n"
                f"BÔNUS DE MAIORIA: {self.majority_bonus}.\n"
                f"BÔNUS TOTAL: {self.totality_bonus}."
            )
        if self.majority_bonus < 0 or self.totality_bonus < 0:
            majority_text = ""
            totality_text = ""
            if self.majority_bonus < 0:
                majority_text = f"BÔNUS DE MAIORIA: {self.majority_bonus}.\n"
            if self.totality_bonus < 0:
                totality_text = f"BÔNUS TOTAL: {self.totality_bonus}."

            raise ValueError(
                "Os bônus devem ser inteiros positivos.\n{}{}".format(
                    majority_text, totality_text
                )
            )

    def __iter__(self):
        yield from self.territories.values()

    def add_territory(self, territory: Territory):
        """Adiciona um território a esse continente."""

        if not isinstance(territory, Territory):
            tt = type(territory)
            logger.warning(f"O território deve ser do tipo Territory ({tt}).")
            return

        if territory.name in self.territories:
            logger.warning(
                f"O território '{territory.name.name}' já pertence "
                f"ao continente '{self.name}'."
            )
            return

        territory.color_emoji = self.color_emoji
        self.territories[territory.name] = territory

    def remove_territory(self, territory_name: TerritoryEnum) -> Territory:
        """Remove um território desse continente."""

        if not isinstance(territory_name, TerritoryEnum):
            tt = type(territory_name)
            raise TypeError(
                f"O território deve ser do tipo TerritoryEnum ({tt})."
            )

        territory = self.territories.pop(territory_name, None)
        territory.color_emoji = None

        return territory

    def get_territory(self, territory_name: TerritoryEnum) -> Territory:
        """Retorna um território desse continente."""

        if not isinstance(territory_name, TerritoryEnum):
            tt = type(territory_name)
            raise TypeError(
                f"O território deve ser do tipo TerritoryEnum ({tt})."
            )

        return self.territories.get(territory_name)

    @property
    def show_name(self) -> str:
        return self.name.name

    @property
    def show_value(self) -> str:
        return self.name.value
