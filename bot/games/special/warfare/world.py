import logging
from typing import Dict, List

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.special.warfare.continent import Continent
from bot.games.special.warfare.territory import Territory

logger = logging.getLogger(__name__)
ce = ContinentEnum
te = TerritoryEnum


class World:
    def __init__(self):
        self.continents = self.create_continents()
        self.territories: Dict[TerritoryEnum, Territory] = {
            territory.name: territory for territory in self.flat_territories()
        }
        self.create_frontiers()

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

    def flat_territories(self) -> List[Territory]:
        return [
            territory
            for continent in self.continents.values()
            for territory in continent.territories.values()
        ]

    def create_africa(self) -> Continent:
        africa_kw_args = {"totality_bonus": 3, "color_emoji": "🟪"}
        africa = Continent(name=ce.AFRICA, **africa_kw_args)
        africa.add_territory(territory=Territory(name=te.ALGERIA))
        africa.add_territory(territory=Territory(name=te.CONGO))
        africa.add_territory(territory=Territory(name=te.EGYPT))
        africa.add_territory(territory=Territory(name=te.MADAGASCAR))
        africa.add_territory(territory=Territory(name=te.SOUTH_AFRICA))
        africa.add_territory(territory=Territory(name=te.SUDAO))

        return africa

    def create_asia(self) -> Continent:
        asia_kw_args = {"totality_bonus": 7, "color_emoji": "🟨"}
        asia = Continent(name=ce.ASIA, **asia_kw_args)
        asia.add_territory(territory=Territory(name=te.ARAL))
        asia.add_territory(territory=Territory(name=te.CHINA))
        asia.add_territory(territory=Territory(name=te.DUDINKA))
        asia.add_territory(territory=Territory(name=te.INDIA))
        asia.add_territory(territory=Territory(name=te.JAPAN))
        asia.add_territory(territory=Territory(name=te.MIDDLE_EAST))
        asia.add_territory(territory=Territory(name=te.MONGOLIA))
        asia.add_territory(territory=Territory(name=te.OMSK))
        asia.add_territory(territory=Territory(name=te.SIBERIA))
        asia.add_territory(territory=Territory(name=te.TCHITA))
        asia.add_territory(territory=Territory(name=te.VIETNAM))
        asia.add_territory(territory=Territory(name=te.VLADIVOSTOK))

        return asia

    def create_europe(self) -> Continent:
        europe_kw_args = {"totality_bonus": 5, "color_emoji": "🟦"}
        europe = Continent(name=ce.EUROPE, **europe_kw_args)
        europe.add_territory(territory=Territory(name=te.ENGLAND))
        europe.add_territory(territory=Territory(name=te.FRANCE))
        europe.add_territory(territory=Territory(name=te.GERMANY))
        europe.add_territory(territory=Territory(name=te.ICELAND))
        europe.add_territory(territory=Territory(name=te.MOSCOW))
        europe.add_territory(territory=Territory(name=te.POLAND))
        europe.add_territory(territory=Territory(name=te.SWEDEN))

        return europe

    def create_north_america(self) -> Continent:
        na_kw_args = {"totality_bonus": 5, "color_emoji": "🟧"}
        north_america = Continent(name=ce.NORTH_AMERICA, **na_kw_args)
        north_america.add_territory(territory=Territory(name=te.ALASCA))
        north_america.add_territory(territory=Territory(name=te.CALIFORNIA))
        north_america.add_territory(territory=Territory(name=te.GREENLAND))
        north_america.add_territory(territory=Territory(name=te.LABRADOR))
        north_america.add_territory(territory=Territory(name=te.MACKENZIE))
        north_america.add_territory(territory=Territory(name=te.MEXICO))
        north_america.add_territory(territory=Territory(name=te.NEW_YORK))
        north_america.add_territory(territory=Territory(name=te.OTTAWA))
        north_america.add_territory(territory=Territory(name=te.VANCOUVER))

        return north_america

    def create_oceania(self) -> Continent:
        oceania_kw_args = {"totality_bonus": 2, "color_emoji": "🟥"}
        oceania = Continent(name=ce.OCEANIA, **oceania_kw_args)
        oceania.add_territory(territory=Territory(name=te.AUSTRALIA))
        oceania.add_territory(territory=Territory(name=te.BORNEO))
        oceania.add_territory(territory=Territory(name=te.NEW_GUINEA))
        oceania.add_territory(territory=Territory(name=te.SUMATRA))

        return oceania

    def create_south_america(self) -> Continent:
        sa_kw_args = {"totality_bonus": 2, "color_emoji": "🟩"}
        south_america = Continent(name=ce.SOUTH_AMERICA, **sa_kw_args)
        south_america.add_territory(territory=Territory(name=te.ARGENTINA))
        south_america.add_territory(territory=Territory(name=te.BRAZIL))
        south_america.add_territory(territory=Territory(name=te.PERU))
        south_america.add_territory(territory=Territory(name=te.VENEZUELA))

        return south_america

    def create_frontiers(self):
        FRONTIER_DICT = {
            # Africa
            te.ALGERIA: [te.BRAZIL, te.CONGO, te.EGYPT, te.FRANCE, te.SUDAO],
            te.CONGO: [te.SOUTH_AFRICA, te.SUDAO],
            te.EGYPT: [te.FRANCE, te.MIDDLE_EAST, te.POLAND, te.SUDAO],
            te.MADAGASCAR: [te.SOUTH_AFRICA, te.SUDAO],
            te.SOUTH_AFRICA: [te.SUDAO],
            te.SUDAO: [],  # EMPTY
            # Asia
            te.ARAL: [te.CHINA, te.INDIA, te.MIDDLE_EAST, te.MOSCOW, te.OMSK],
            te.CHINA: [
                te.INDIA,
                te.JAPAN,
                te.MONGOLIA,
                te.OMSK,
                te.TCHITA,
                te.VIETNAM,
                te.VLADIVOSTOK,
            ],
            te.DUDINKA: [te.MONGOLIA, te.OMSK, te.SIBERIA, te.TCHITA],
            te.INDIA: [te.MIDDLE_EAST, te.SUMATRA, te.VIETNAM],
            te.JAPAN: [te.VLADIVOSTOK],
            te.MIDDLE_EAST: [te.MOSCOW, te.POLAND],
            te.MONGOLIA: [te.OMSK, te.TCHITA],
            te.OMSK: [te.MOSCOW],
            te.SIBERIA: [te.TCHITA, te.VLADIVOSTOK],
            te.TCHITA: [te.VLADIVOSTOK],
            te.VIETNAM: [te.BORNEO],
            te.VLADIVOSTOK: [te.ALASCA],
            # Europe
            te.ENGLAND: [te.FRANCE, te.GERMANY, te.ICELAND, te.SWEDEN],
            te.FRANCE: [te.GERMANY, te.POLAND],
            te.GERMANY: [te.POLAND],
            te.ICELAND: [te.GREENLAND],
            te.MOSCOW: [te.POLAND, te.SWEDEN],
            te.POLAND: [],  # EMPTY
            te.SWEDEN: [],  # EMPTY
            # North America
            te.ALASCA: [te.MACKENZIE, te.VANCOUVER],
            te.CALIFORNIA: [te.MEXICO, te.NEW_YORK, te.OTTAWA, te.VANCOUVER],
            te.GREENLAND: [te.LABRADOR, te.MACKENZIE],
            te.LABRADOR: [te.NEW_YORK, te.OTTAWA],
            te.MACKENZIE: [te.OTTAWA, te.VANCOUVER],
            te.MEXICO: [te.NEW_YORK, te.VENEZUELA],
            te.NEW_YORK: [te.OTTAWA],
            te.OTTAWA: [te.VANCOUVER],
            te.VANCOUVER: [],  # EMPTY
            # Oceania
            te.AUSTRALIA: [te.BORNEO, te.NEW_GUINEA, te.SUMATRA],
            te.BORNEO: [te.NEW_GUINEA],
            te.NEW_GUINEA: [],  # EMPTY
            te.SUMATRA: [],  # EMPTY
            # South America
            te.ARGENTINA: [te.BRAZIL, te.PERU],
            te.BRAZIL: [te.PERU, te.VENEZUELA],
            te.PERU: [te.VENEZUELA],
            te.VENEZUELA: [],  # EMPTY
        }

        for territory_enum, frontier_enum_list in FRONTIER_DICT.items():
            for frontier_enum in frontier_enum_list:
                territory = self.territories[territory_enum]
                frontier_territory = self.territories[frontier_enum]
                territory.add_frontier(frontier_territory)
