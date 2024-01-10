'''
Utils - serializer, map access
'''

from model.map import Map
from model.anthill import Anthill
from model.ant import Ant
from model.player import Player
from model.color import Color as cl

from os import listdir
import re
import jsonpickle


PLAYER_COLORS = [cl.BLUE, cl.RED, cl.CYAN, cl.ORANGE, cl.PINK, cl.BROWN, cl.PURPLE]

MAP_URL = './maps/'

def map_to_json(map : Map):
    '''Converts map to json'''
    return jsonpickle.encode(map, indent=4, unpicklable=True, make_refs=True, keys=True, )

def json_to_map(json : str):
    '''Converts json to Map object'''
    return jsonpickle.decode(json, classes=[Map, Anthill, Player, Ant], keys=True)

def retrieve_map(id):
    '''Gets map by id from map folder'''
    map_names = listdir(MAP_URL)
    re_map = re.compile(f"^map_{id}.txt")
    if len(list(filter(re_map.match, map_names))) > 0:
        with open(f'{MAP_URL}map_{id}.txt', 'r') as f:
            return json_to_map(f.read())
    return None

def assign_color_to_players(list_of_players):
    '''Assigns free colors to enemies'''
    player_color = {}
    if len(list_of_players) > len(PLAYER_COLORS):
        raise RuntimeError('not enough colors for players')
    for i, player in enumerate(list_of_players):
        player_color[player] = PLAYER_COLORS[:][i]
    return player_color
