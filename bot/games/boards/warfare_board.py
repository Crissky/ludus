
from dataclasses import dataclass, field

from networkx import Graph

from bot.games.player import Player

world_graph = Graph()

@dataclass
class territory:
    name: str
    world_graph: Graph
    occupier: Player = None
    troops: int = 0


@dataclass
class continent:
    name: str
    world_graph: Graph
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
class world:
    world_graph: Graph
    continents: list = field(default_factory=list)

    def __post_init__(self):
        self.territories = []
        for cont in self.continents:
            self.territories.extend(cont.territories)
