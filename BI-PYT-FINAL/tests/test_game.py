'''Game manager tests'''

import pytest
from flexmock import flexmock
from model.player import Player
from model.map import Map
from model.ant import Ant
from model.anthill import Anthill
from game import __get_colliding_ants, __choose_source, __enemy_info, __choose_target, simulate_players
import game as game_module

@pytest.fixture
def players():
    '''
    return players (first is owner)
    '''
    return [Player('Karel'), Player('Lucka'), Player('Marek')]


def test_simulate_players(players):
    '''test simulation sleects target and source'''
    ah_map = Map()
    owner = players[0]
    enemy = players[1]
  
    anthill1 = Anthill(owner, population=20, available_ants=10)
    anthill2 = Anthill(owner, population=20, available_ants=10)
    anthill3 = Anthill(enemy, population=20, available_ants=10)
    ah_map.anthills = [anthill1, anthill2, anthill3]
    ah_map.player_ahs = { owner : [anthill1, anthill2], enemy: [anthill3]}

    flexmock(game_module).should_call('__choose_source').at_least().once()
    flexmock(game_module).should_call('__choose_target').at_least().once()
    simulate_players([owner, enemy], ah_map)


def test____get_colliding_ants(players):
    '''test ant collisions on map (ant-ant, ant-anthill)'''
    ah_map = Map()
    owner = players[0]
    enemy = players[1]

    ah_width = 10
    ant_width = 6
    anthill1 = Anthill(owner, population=20, x_loc=5, y_loc=5, width=ah_width, height=ah_width)
    anthill2 = Anthill(enemy, population=20, x_loc=60, y_loc=60, width=ah_width, height=ah_width)
    anthill3 = Anthill(owner, population=20, x_loc=5, y_loc=25, width=ah_width, height=ah_width)

    ah_map.ah_coords = {anthill1 : (5,5), anthill2 : (50,50), anthill3 : (5,25)}

    ant1 = Ant(x_loc = 10, y_loc = 10, owner = owner, width=ant_width, height=ant_width, from_ah= anthill1, to_ah=anthill2)
    ant2 = Ant(x_loc = 11, y_loc = 11, owner = owner, width=ant_width, height=ant_width,  from_ah= anthill1, to_ah=anthill2)
    ant3 = Ant(x_loc = 20, y_loc = 20, owner = owner, width=ant_width, height=ant_width,  from_ah= anthill1, to_ah=anthill2)
    ant4 = Ant(x_loc = 9, y_loc = 9, owner = enemy, width=ant_width, height=ant_width, from_ah= anthill2, to_ah=anthill1)
    ant5 = Ant(x_loc = 41, y_loc = 41, owner = enemy, width=ant_width, height=ant_width, from_ah= anthill2, to_ah=anthill1)
    ant6 = Ant(x_loc = 22, y_loc = 22, owner = enemy, width=ant_width, height=ant_width, from_ah= anthill2, to_ah=anthill1)
    ant7 = Ant(x_loc = 5, y_loc = 20, owner = owner, width=ant_width, height=ant_width,  from_ah= anthill1, to_ah=anthill3)
    
    # friendly collide ah
    ants = [ant1, ant2, ant3, ant7]
    ah_map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(ah_map)
    assert colliding_ant == set([ant7])

    # enemy collide ah
    ants = [ant4]
    ah_map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(ah_map)
    assert colliding_ant == set([ant4])
    
    # two enemy collide
    ants = [ant3, ant6]
    ah_map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(ah_map)
    assert colliding_ant == set([ant3, ant6])

    # two friendly
    ants = [ant5, ant6]
    ah_map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(ah_map)
    assert colliding_ant == set()

def test___choose_source(players):
    '''test source'''

    anthill1 = Anthill(players[0], 20, 15)
    anthill1 = flexmock(anthill1)
    anthill1.should_call('get_population')
    anthill2 = Anthill(players[0], 20, 20)
    anthill2 = flexmock(anthill2)
    anthill2.should_call('get_population')
    anthill3 = Anthill(players[0], 30, 10)
    anthill3 = flexmock(anthill3)
    anthill3.should_call('get_population')

    source, _, _ = __choose_source([anthill1, anthill2, anthill3])
    assert source == anthill2

def test___choose_target(players):
    ah_map = Map()
    owner = players[0]
    enemy1 = players[1]
    enemy2 = players[2]

    anthill1 = Anthill(owner, population=20, available_ants=20)
    anthill2 = Anthill(enemy1, population=20, available_ants=20)
    anthill3 = Anthill(enemy2, population=30, available_ants=5)
    anthill4 = Anthill(owner, population=10, available_ants=10)
    anthill5 = Anthill(enemy2, population=10, available_ants=8)

    anthills = [anthill1, anthill2, anthill3, anthill4, anthill5]

    ah_map.player_ahs = {}
    for ah in anthills:
        if ah.owner in ah_map.player_ahs:
            ah_map.player_ahs[ah.owner].append(ah)
        else:
            ah_map.player_ahs[ah.owner] = [ah]

    source, _, min_i = __choose_source(ah_map.player_ahs[owner])
    assert source == anthill1

    # attack weakest enemy
    to_ah = __choose_target(ah_map.player_ahs[owner], [owner, enemy1, enemy2], source, owner, min_i, ah_map)
    assert to_ah == anthill2

    anthill4.population = 3
    anthill4.available_ants = 3
    # help low health anthill
    to_ah = __choose_target(ah_map.player_ahs[owner], [owner, enemy1, enemy2], source, owner, min_i, ah_map)
    assert to_ah == anthill4

    anthill1.population = 3
    anthill1.available_ants = 3
    source, _, min_i = __choose_source(ah_map.player_ahs[owner])
    # low health, dont attack
    to_ah = __choose_target(ah_map.player_ahs[owner], [owner, enemy1, enemy2], source, owner, min_i, ah_map)
    assert to_ah is None

def test___choose_target_no_ah(players):

    ah_map = Map()
    owner = players[0]
    enemy1 = players[1]
    anthill1 = Anthill(owner, population=20, available_ants=20)
    anthill2 = Anthill(owner, population=10, available_ants=10)

    ah_map.player_ahs = {owner: [anthill1, anthill2], enemy1: []}

    source, _, min_i = __choose_source(ah_map.player_ahs[owner])
    # attack weakest enemy
    to_ah = __choose_target(ah_map.player_ahs[owner], [owner, enemy1], source, owner, min_i, ah_map)
    assert to_ah is None

def test___enemy_info(players):
    ah_map = Map()

    owner = players[0]
    enemy1 = players[1]
    enemy2 = players[2]
    anthill1 = Anthill(owner, population=20, available_ants=20)
    anthill2 = Anthill(enemy1, population=20, available_ants=20)
    anthill3 = Anthill(enemy2, population=30, available_ants=5)
    anthill4 = Anthill(owner, population=10, available_ants=10)
    anthill5 = Anthill(enemy2, population=10, available_ants=8)

    anthills = [anthill1, anthill2, anthill3, anthill4, anthill5]
    ah_map.player_ahs = {}
    for ah in anthills:
        if ah.owner in ah_map.player_ahs:
            ah_map.player_ahs[ah.owner].append(ah)
        else:
            ah_map.player_ahs[ah.owner] = [ah]


    sums, mins = __enemy_info([owner, enemy1, enemy2], owner, ah_map)
    assert len(sums) == 3
    assert len(mins) == 3
    assert sums[0] == float('inf')
    assert mins[0] == float('inf')
    assert sums[1] == 20
    assert ah_map.player_ahs[enemy1][mins[1]] == anthill2
    assert sums[2] == 40
    assert ah_map.player_ahs[enemy2][mins[2]] == anthill5
