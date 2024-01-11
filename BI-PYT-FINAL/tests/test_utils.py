'''Utils tests'''

import pytest
from utils import *
from model.map import Map


@pytest.mark.run(after='test_serialization')
def test_load_map():
    '''
    get map by id
    '''
    ah_map = retrieve_map(100)
    assert ah_map is not None

    ah_map = retrieve_map(0)
    assert ah_map is None


def test_serialization():
    '''
    naive
    map -> json, json -> map
    '''

    t_map = Map([Anthill(Player('Karel'), 20, 20)])

    json_map = map_to_json(t_map)
    assert isinstance(json_map, str)

    parsed_t_map = json_to_map(json_map)
    assert isinstance(parsed_t_map, Map)

    assert len(parsed_t_map.anthills) == 1
    assert t_map.anthills[0].get_population(False) == parsed_t_map.anthills[0].get_population(False)



def test_colors():
    '''
    test colors
    '''
    players = [Player("Pepa"), Player("Jana"), Player("Adolf"), None]
    player_colors = assign_color_to_players(players)

    assert isinstance(player_colors, dict)
    
    assert len(players) == len(player_colors.keys())
    assert len(players) == len(player_colors.values())
    assert set(players) == set(player_colors.keys())

    for player, color in player_colors.items():
        assert player in players
        assert color in PLAYER_COLORS
