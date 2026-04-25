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

africa = Continent(name=ce.AFRICA, totality_bonus=3)
asia = Continent(name=ce.ASIA, totality_bonus=7)
europa = Continent(name=ce.EUROPA, totality_bonus=5)
north_america = Continent(name=ce.NORTH_AMERICA, totality_bonus=5)
oceania = Continent(name=ce.OCEANIA, totality_bonus=2)
south_america = Continent(name=ce.SOUTH_AMERICA, totality_bonus=2)
CONTINENTS = {
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

