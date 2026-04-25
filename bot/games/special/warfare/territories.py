"""
Territórios do jogo Warfare

Mapa referência WAR: https://a-static.mlcdn.com.br/1500x1500/jogo-war-de-tabuleiro-o-jogo-da-estrategia-war-edicao-especial-grow/magazineluiza/220544300/5f103a8a5eaaf72543b083b6d557f693.jpg
Mapa referência WAR II: https://a-static.mlcdn.com.br/1500x1500/jogo-war-ii-tabuleiro-o-jogo-da-estrategia-com-batalhas-aereas-grow/magazineluiza/220544400/9ef9916b944c31e3fb02ed68919bc7c5.jpg
"""

from bot.games.enums.warfare import ContinentEnum, TerritoryEnum
from bot.games.special.warfare.territory import Territory

ce = ContinentEnum
te = TerritoryEnum

AFRICA = {}
ASIA = {}
EUROPA = {}
NORTH_AMERICA = {}
OCEANIA = {}
SOUTH_AMERICA = {}
TERRITORIES = {
    ContinentEnum.ASIA: ASIA,
    ContinentEnum.AFRICA: AFRICA,
    ContinentEnum.EUROPA: EUROPA,
    ContinentEnum.NORTH_AMERICA: NORTH_AMERICA,
    ContinentEnum.OCEANIA: OCEANIA,
    ContinentEnum.SOUTH_AMERICA: SOUTH_AMERICA,
}


# Africa
AFRICA[te.ALGERIA] = Territory(name=te.ALGERIA)
AFRICA[te.CONGO] = Territory(name=te.CONGO)
AFRICA[te.EGYPT] = Territory(name=te.EGYPT)
AFRICA[te.MADAGASCAR] = Territory(name=te.MADAGASCAR)
AFRICA[te.SOUTH_AFRICA] = Territory(name=te.SOUTH_AFRICA)
AFRICA[te.SUDAO] = Territory(name=te.SUDAO)

# Asia
ASIA[te.ARAL] = Territory(name=te.ARAL)
ASIA[te.CHINA] = Territory(name=te.CHINA)
ASIA[te.DUDINKA] = Territory(name=te.DUDINKA)
ASIA[te.INDIA] = Territory(name=te.INDIA)
ASIA[te.JAPAN] = Territory(name=te.JAPAN)
ASIA[te.MIDDLE_EAST] = Territory(name=te.MIDDLE_EAST)
ASIA[te.MONGOLIA] = Territory(name=te.MONGOLIA)
ASIA[te.OMSK] = Territory(name=te.OMSK)
ASIA[te.SIBERIA] = Territory(name=te.SIBERIA)
ASIA[te.TCHITA] = Territory(name=te.TCHITA)
ASIA[te.VIETNAM] = Territory(name=te.VIETNAM)
ASIA[te.VLADIVOSTOK] = Territory(name=te.VLADIVOSTOK)

# Europa
EUROPA[te.ENGLAND] = Territory(name=te.ENGLAND)
EUROPA[te.FRANCE] = Territory(name=te.FRANCE)
EUROPA[te.GERMANY] = Territory(name=te.GERMANY)
EUROPA[te.ICELAND] = Territory(name=te.ICELAND)
EUROPA[te.MOSCOW] = Territory(name=te.MOSCOW)
EUROPA[te.POLAND] = Territory(name=te.POLAND)
EUROPA[te.SWEDEN] = Territory(name=te.SWEDEN)

# North America
NORTH_AMERICA[te.ALASCA] = Territory(name=te.ALASCA)
NORTH_AMERICA[te.CALIFORNIA] = Territory(name=te.CALIFORNIA)
NORTH_AMERICA[te.GREENLAND] = Territory(name=te.GREENLAND)
NORTH_AMERICA[te.LABRADOR] = Territory(name=te.LABRADOR)
NORTH_AMERICA[te.MACKENZIE] = Territory(name=te.MACKENZIE)
NORTH_AMERICA[te.MEXICO] = Territory(name=te.MEXICO)
NORTH_AMERICA[te.NEW_YORK] = Territory(name=te.NEW_YORK)
NORTH_AMERICA[te.OTTAWA] = Territory(name=te.OTTAWA)
NORTH_AMERICA[te.VANCOUVER] = Territory(name=te.VANCOUVER)

# Oceania
OCEANIA[te.AUSTRALIA] = Territory(name=te.AUSTRALIA)
OCEANIA[te.BORNEO] = Territory(name=te.BORNEO)
OCEANIA[te.NEW_GUINEA] = Territory(name=te.NEW_GUINEA)
OCEANIA[te.SUMATRA] = Territory(name=te.SUMATRA)

# South America
SOUTH_AMERICA[te.ARGENTINA] = Territory(name=te.ARGENTINA)
SOUTH_AMERICA[te.BRAZIL] = Territory(name=te.BRAZIL)
SOUTH_AMERICA[te.PERU] = Territory(name=te.PERU)
SOUTH_AMERICA[te.VENEZUELA] = Territory(name=te.VENEZUELA)
