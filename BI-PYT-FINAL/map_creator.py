'''
Creator for maps
'''

from model.map import Map
from model.anthill import Anthill
from model.player import Player
from utils import assign_color_to_players, map_to_json, MAP_URL


def create_map(id):
    '''Map_creator'''

    map = Map()
    # CREATE MAP

    a1 = Anthill(None, 20, 20)
    a2 = Anthill(None, 20, 20)
    pl1 = Player('Gustav')
    pl2 = Player('Bob')
    map.players.append(pl1)
    map.players.append(pl2)
    a3 = Anthill(pl1, 20, 20)
    a4 = Anthill(pl1, 20, 20)
    a5 = Anthill(pl2, 20, 20)
    a6 = Anthill(pl2, 20, 20)
    map.place_anthill(a1, 150, 10)
    map.place_anthill(a2, 100, 230)
    map.place_anthill(a3, 20, 70)
    map.place_anthill(a4, 30, 150)
    map.place_anthill(a5, 210, 80)
    map.place_anthill(a6, 230, 180)

    pl_cl = assign_color_to_players(map.players)
    map.player_colors = pl_cl

    json_map = map_to_json(map)
    try:
        with open(f'{MAP_URL}map_{id}.txt', 'w', encoding='UTF8') as f:
            f.write(json_map)
            return True
    except:
        raise Exception('Map not saved')

if __name__ == '__main__':
    create_map(102)
