"""
Territórios do jogo Warfare

Mapa referência WAR: https://a-static.mlcdn.com.br/1500x1500/jogo-war-de-tabuleiro-o-jogo-da-estrategia-war-edicao-especial-grow/magazineluiza/220544300/5f103a8a5eaaf72543b083b6d557f693.jpg
Mapa referência WAR II: https://a-static.mlcdn.com.br/1500x1500/jogo-war-ii-tabuleiro-o-jogo-da-estrategia-com-batalhas-aereas-grow/magazineluiza/220544400/9ef9916b944c31e3fb02ed68919bc7c5.jpg
"""

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.special.warfare.continent import Continent
from bot.games.special.warfare.territory import Territory

ce = ContinentEnum
te = TerritoryEnum

africa_kw_args = {"totality_bonus": 3, "color_emoji": "🟪"}
asia_kw_args = {"totality_bonus": 7, "color_emoji": "🟨"}
europa_kw_args = {"totality_bonus": 5, "color_emoji": "🟦"}
north_america_kw_args = {"totality_bonus": 5, "color_emoji": "🟧"}
oceania_kw_args = {"totality_bonus": 2, "color_emoji": "🟥"}
south_america_kw_args = {"totality_bonus": 2, "color_emoji": "🟩"}

africa = Continent(name=ce.AFRICA, **africa_kw_args)
asia = Continent(name=ce.ASIA, **asia_kw_args)
europa = Continent(name=ce.EUROPA, **europa_kw_args)
north_america = Continent(name=ce.NORTH_AMERICA, **north_america_kw_args)
oceania = Continent(name=ce.OCEANIA, **oceania_kw_args)
south_america = Continent(name=ce.SOUTH_AMERICA, **south_america_kw_args)
CONTINENT_DICT = {
    ContinentEnum.ASIA: asia,
    ContinentEnum.AFRICA: africa,
    ContinentEnum.EUROPA: europa,
    ContinentEnum.NORTH_AMERICA: north_america,
    ContinentEnum.OCEANIA: oceania,
    ContinentEnum.SOUTH_AMERICA: south_america,
}

# Africa
africa.add_territory(territory=Territory(name=te.ALGERIA))
africa.add_territory(territory=Territory(name=te.CONGO))
africa.add_territory(territory=Territory(name=te.EGYPT))
africa.add_territory(territory=Territory(name=te.MADAGASCAR))
africa.add_territory(territory=Territory(name=te.SOUTH_AFRICA))
africa.add_territory(territory=Territory(name=te.SUDAO))

# Asia
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

# Europa
europa.add_territory(territory=Territory(name=te.ENGLAND))
europa.add_territory(territory=Territory(name=te.FRANCE))
europa.add_territory(territory=Territory(name=te.GERMANY))
europa.add_territory(territory=Territory(name=te.ICELAND))
europa.add_territory(territory=Territory(name=te.MOSCOW))
europa.add_territory(territory=Territory(name=te.POLAND))
europa.add_territory(territory=Territory(name=te.SWEDEN))

# North America
north_america.add_territory(territory=Territory(name=te.ALASCA))
north_america.add_territory(territory=Territory(name=te.CALIFORNIA))
north_america.add_territory(territory=Territory(name=te.GREENLAND))
north_america.add_territory(territory=Territory(name=te.LABRADOR))
north_america.add_territory(territory=Territory(name=te.MACKENZIE))
north_america.add_territory(territory=Territory(name=te.MEXICO))
north_america.add_territory(territory=Territory(name=te.NEW_YORK))
north_america.add_territory(territory=Territory(name=te.OTTAWA))
north_america.add_territory(territory=Territory(name=te.VANCOUVER))

# Oceania
oceania.add_territory(territory=Territory(name=te.AUSTRALIA))
oceania.add_territory(territory=Territory(name=te.BORNEO))
oceania.add_territory(territory=Territory(name=te.NEW_GUINEA))
oceania.add_territory(territory=Territory(name=te.SUMATRA))

# South America
south_america.add_territory(territory=Territory(name=te.ARGENTINA))
south_america.add_territory(territory=Territory(name=te.BRAZIL))
south_america.add_territory(territory=Territory(name=te.PERU))
south_america.add_territory(territory=Territory(name=te.VENEZUELA))

# Frontiers
FRONTIER_DICT = {
    # Africa
    te.ALGERIA: [te.BRAZIL, te.CONGO, te.EGYPT, te.FRANCE, te.SUDAO],
    te.CONGO: [te.SOUTH_AFRICA, te.SUDAO],
    te.EGYPT: [te.FRANCE, te.MIDDLE_EAST, te.POLAND, te.SUDAO],
    te.MADAGASCAR: [te.SOUTH_AFRICA, te.SUDAO],
    te.SOUTH_AFRICA: [te.SUDAO],
    te.SUDAO: [],
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
    # Europa
    te.ENGLAND: [],
    te.FRANCE: [],
    te.GERMANY: [],
    te.ICELAND: [],
    te.MOSCOW: [],
    te.POLAND: [],
    te.SWEDEN: [],
    # North America
    te.ALASCA: [],
    te.CALIFORNIA: [],
    te.GREENLAND: [],
    te.LABRADOR: [],
    te.MACKENZIE: [],
    te.MEXICO: [],
    te.NEW_YORK: [],
    te.OTTAWA: [],
    te.VANCOUVER: [],
    # Oceania
    te.AUSTRALIA: [],
    te.BORNEO: [],
    te.NEW_GUINEA: [],
    te.SUMATRA: [],
    # South America
    te.ARGENTINA: [],
    te.BRAZIL: [],
    te.PERU: [],
    te.VENEZUELA: [],
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

for territory in sorted(territories.values(), key=lambda x: x.name.name):
    print(territory.show_name, [t.name for t in territory.frontiers])
