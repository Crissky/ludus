"""
Territórios do jogo Warfare

Mapa referência WAR: https://a-static.mlcdn.com.br/1500x1500/jogo-war-de-tabuleiro-o-jogo-da-estrategia-war-edicao-especial-grow/magazineluiza/220544300/5f103a8a5eaaf72543b083b6d557f693.jpg
Mapa referência WAR II: https://a-static.mlcdn.com.br/1500x1500/jogo-war-ii-tabuleiro-o-jogo-da-estrategia-com-batalhas-aereas-grow/magazineluiza/220544400/9ef9916b944c31e3fb02ed68919bc7c5.jpg
"""

from operator import attrgetter

from bot.games.enums.warfare import ContinentNames, TerritoryNames
from bot.games.special.warfare.continent import Continent
from bot.games.special.warfare.territory import Territory

cn = ContinentNames
tn = TerritoryNames

africa_kw_args = {"totality_bonus": 3, "color_emoji": "🟪"}
asia_kw_args = {"totality_bonus": 7, "color_emoji": "🟨"}
europe_kw_args = {"totality_bonus": 5, "color_emoji": "🟦"}
north_america_kw_args = {"totality_bonus": 5, "color_emoji": "🟧"}
oceania_kw_args = {"totality_bonus": 2, "color_emoji": "🟥"}
south_america_kw_args = {"totality_bonus": 2, "color_emoji": "🟩"}

africa = Continent(name=cn.AFRICA, **africa_kw_args)
asia = Continent(name=cn.ASIA, **asia_kw_args)
europe = Continent(name=cn.EUROPE, **europe_kw_args)
north_america = Continent(name=cn.NORTH_AMERICA, **north_america_kw_args)
oceania = Continent(name=cn.OCEANIA, **oceania_kw_args)
south_america = Continent(name=cn.SOUTH_AMERICA, **south_america_kw_args)
CONTINENT_DICT = {
    ContinentNames.ASIA: asia,
    ContinentNames.AFRICA: africa,
    ContinentNames.EUROPE: europe,
    ContinentNames.NORTH_AMERICA: north_america,
    ContinentNames.OCEANIA: oceania,
    ContinentNames.SOUTH_AMERICA: south_america,
}

# Africa
africa.add_territory(territory=Territory(name=tn.ALGERIA))
africa.add_territory(territory=Territory(name=tn.CONGO))
africa.add_territory(territory=Territory(name=tn.EGYPT))
africa.add_territory(territory=Territory(name=tn.MADAGASCAR))
africa.add_territory(territory=Territory(name=tn.SOUTH_AFRICA))
africa.add_territory(territory=Territory(name=tn.SUDAO))

# Asia
asia.add_territory(territory=Territory(name=tn.ARAL))
asia.add_territory(territory=Territory(name=tn.CHINA))
asia.add_territory(territory=Territory(name=tn.DUDINKA))
asia.add_territory(territory=Territory(name=tn.INDIA))
asia.add_territory(territory=Territory(name=tn.JAPAN))
asia.add_territory(territory=Territory(name=tn.MIDDLE_EAST))
asia.add_territory(territory=Territory(name=tn.MONGOLIA))
asia.add_territory(territory=Territory(name=tn.OMSK))
asia.add_territory(territory=Territory(name=tn.SIBERIA))
asia.add_territory(territory=Territory(name=tn.TCHITA))
asia.add_territory(territory=Territory(name=tn.VIETNAM))
asia.add_territory(territory=Territory(name=tn.VLADIVOSTOK))

# Europe
europe.add_territory(territory=Territory(name=tn.ENGLAND))
europe.add_territory(territory=Territory(name=tn.FRANCE))
europe.add_territory(territory=Territory(name=tn.GERMANY))
europe.add_territory(territory=Territory(name=tn.ICELAND))
europe.add_territory(territory=Territory(name=tn.MOSCOW))
europe.add_territory(territory=Territory(name=tn.POLAND))
europe.add_territory(territory=Territory(name=tn.SWEDEN))

# North America
north_america.add_territory(territory=Territory(name=tn.ALASCA))
north_america.add_territory(territory=Territory(name=tn.CALIFORNIA))
north_america.add_territory(territory=Territory(name=tn.GREENLAND))
north_america.add_territory(territory=Territory(name=tn.LABRADOR))
north_america.add_territory(territory=Territory(name=tn.MACKENZIE))
north_america.add_territory(territory=Territory(name=tn.MEXICO))
north_america.add_territory(territory=Territory(name=tn.NEW_YORK))
north_america.add_territory(territory=Territory(name=tn.OTTAWA))
north_america.add_territory(territory=Territory(name=tn.VANCOUVER))

# Oceania
oceania.add_territory(territory=Territory(name=tn.AUSTRALIA))
oceania.add_territory(territory=Territory(name=tn.BORNEO))
oceania.add_territory(territory=Territory(name=tn.NEW_GUINEA))
oceania.add_territory(territory=Territory(name=tn.SUMATRA))

# South America
south_america.add_territory(territory=Territory(name=tn.ARGENTINA))
south_america.add_territory(territory=Territory(name=tn.BRAZIL))
south_america.add_territory(territory=Territory(name=tn.PERU))
south_america.add_territory(territory=Territory(name=tn.VENEZUELA))

# Frontiers
FRONTIER_DICT = {
    # Africa
    tn.ALGERIA: [tn.BRAZIL, tn.CONGO, tn.EGYPT, tn.FRANCE, tn.SUDAO],
    tn.CONGO: [tn.SOUTH_AFRICA, tn.SUDAO],
    tn.EGYPT: [tn.FRANCE, tn.MIDDLE_EAST, tn.POLAND, tn.SUDAO],
    tn.MADAGASCAR: [tn.SOUTH_AFRICA, tn.SUDAO],
    tn.SOUTH_AFRICA: [tn.SUDAO],
    tn.SUDAO: [],  # EMPTY
    # Asia
    tn.ARAL: [tn.CHINA, tn.INDIA, tn.MIDDLE_EAST, tn.MOSCOW, tn.OMSK],
    tn.CHINA: [
        tn.INDIA,
        tn.JAPAN,
        tn.MONGOLIA,
        tn.OMSK,
        tn.TCHITA,
        tn.VIETNAM,
        tn.VLADIVOSTOK,
    ],
    tn.DUDINKA: [tn.MONGOLIA, tn.OMSK, tn.SIBERIA, tn.TCHITA],
    tn.INDIA: [tn.MIDDLE_EAST, tn.SUMATRA, tn.VIETNAM],
    tn.JAPAN: [tn.VLADIVOSTOK],
    tn.MIDDLE_EAST: [tn.MOSCOW, tn.POLAND],
    tn.MONGOLIA: [tn.OMSK, tn.TCHITA],
    tn.OMSK: [tn.MOSCOW],
    tn.SIBERIA: [tn.TCHITA, tn.VLADIVOSTOK],
    tn.TCHITA: [tn.VLADIVOSTOK],
    tn.VIETNAM: [tn.BORNEO],
    tn.VLADIVOSTOK: [tn.ALASCA],
    # Europe
    tn.ENGLAND: [tn.FRANCE, tn.GERMANY, tn.ICELAND, tn.SWEDEN],
    tn.FRANCE: [tn.GERMANY, tn.POLAND],
    tn.GERMANY: [tn.POLAND],
    tn.ICELAND: [tn.GREENLAND],
    tn.MOSCOW: [tn.POLAND, tn.SWEDEN],
    tn.POLAND: [],  # EMPTY
    tn.SWEDEN: [],  # EMPTY
    # North America
    tn.ALASCA: [tn.MACKENZIE, tn.VANCOUVER],
    tn.CALIFORNIA: [tn.MEXICO, tn.NEW_YORK, tn.OTTAWA, tn.VANCOUVER],
    tn.GREENLAND: [tn.LABRADOR, tn.MACKENZIE],
    tn.LABRADOR: [tn.NEW_YORK, tn.OTTAWA],
    tn.MACKENZIE: [tn.OTTAWA, tn.VANCOUVER],
    tn.MEXICO: [tn.NEW_YORK, tn.VENEZUELA],
    tn.NEW_YORK: [tn.OTTAWA],
    tn.OTTAWA: [tn.VANCOUVER],
    tn.VANCOUVER: [],  # EMPTY
    # Oceania
    tn.AUSTRALIA: [tn.BORNEO, tn.NEW_GUINEA, tn.SUMATRA],
    tn.BORNEO: [tn.NEW_GUINEA],
    tn.NEW_GUINEA: [],  # EMPTY
    tn.SUMATRA: [],  # EMPTY
    # South America
    tn.ARGENTINA: [tn.BRAZIL, tn.PERU],
    tn.BRAZIL: [tn.PERU, tn.VENEZUELA],
    tn.PERU: [tn.VENEZUELA],
    tn.VENEZUELA: [],  # EMPTY
}

territories = {
    territory.name: territory
    for continent in CONTINENT_DICT.values()
    for territory in continent
}


for territory_enum, frontier_enum_list in FRONTIER_DICT.items():
    for frontier_enum in frontier_enum_list:
        territory = territories[territory_enum]
        frontier_territory = territories[frontier_enum]
        territory.add_frontier(frontier_territory)

for territory in sorted(territories.values(), key=attrgetter("name.name")):
    print(
        territory.show_name,
        [t.name for t in sorted(territory.frontiers, key=attrgetter("name"))],
    )
