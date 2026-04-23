import logging
from typing import List

from bot.games.special.warfare.continent import Continent

logger = logging.getLogger(__name__)


class World:
    def __init__(self):
        self.continents = self.create_continents()
        self.territories = self.flat_territories(self.continents)

    def create_continents(self) -> List[Continent]:
        africa = self.create_africa()
        asia = self.create_asia()
        europe = self.create_europe()
        north_america = self.create_north_america()
        oceania = self.create_oceania()
        south_america = self.create_south_america()

        return [
            africa,
            asia,
            europe,
            north_america,
            oceania,
            south_america,
        ]

    def flat_territories(self, continents: List[Continent]):
        return [
            territory
            for continent in continents
            for territory in continent.territories
        ]

    def create_africa(self) -> Continent: ...
    def create_asia(self) -> Continent: ...
    def create_europe(self) -> Continent: ...
    def create_north_america(self) -> Continent: ...
    def create_oceania(self) -> Continent: ...
    def create_south_america(self) -> Continent: ...
