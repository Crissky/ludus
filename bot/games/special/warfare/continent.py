import logging

from dataclasses import dataclass, field
from typing import Dict, List, Union

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.special.warfare.territory import Territory


logger = logging.getLogger(__name__)


@dataclass
class Continent:
    name: Union[str, ContinentEnum]
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
