import logging
from typing import Dict, List

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.special.warfare.continent import Continent

logger = logging.getLogger(__name__)


class World:
    def __init__(self):
        self.continents = self.create_continents()

    def __iter__(self):
        yield from self.continents.values()

    def create_continents(self) -> Dict[ContinentEnum, Continent]:
        africa = self.create_africa()
        asia = self.create_asia()
        europe = self.create_europe()
        north_america = self.create_north_america()
        oceania = self.create_oceania()
        south_america = self.create_south_america()

        return {
            ce.AFRICA: africa,
            ce.ASIA: asia,
            ce.EUROPE: europe,
            ce.NORTH_AMERICA: north_america,
            ce.OCEANIA: oceania,
            ce.SOUTH_AMERICA: south_america,
        }

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
