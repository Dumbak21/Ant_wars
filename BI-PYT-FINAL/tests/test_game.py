import pytest
from flexmock import flexmock
from game import __get_colliding_ants, __choose_source, __enemy_info, __choose_target


def test____get_colliding_ants():
    map = flexmock()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy = flexmock(name='Monika', lost_ah=lambda: None, gained_ah=lambda: None)
    ah_width = 10
    ant_width = 6
    anthill1 = flexmock(owner=owner, population=20, x_loc=5, y_loc=5, width=ah_width, height=ah_width, kill_ants=lambda x:None)
    anthill2 = flexmock(owner=enemy, population=20, x_loc=60, y_loc=60, width=ah_width, height=ah_width, kill_ants=lambda x:None)

    map.ah_coords = {anthill1 : (5,5), anthill2 : (50,50)}

    ant1 = flexmock(x_loc = 10, y_loc = 10, owner = owner, width=ant_width, height=ant_width, from_ah= anthill1, to_ah=anthill2)
    ant2 = flexmock(x_loc = 11, y_loc = 11, owner = owner, width=ant_width, height=ant_width,  from_ah= anthill1, to_ah=anthill2)
    ant3 = flexmock(x_loc = 20, y_loc = 20, owner = owner, width=ant_width, height=ant_width,  from_ah= anthill1, to_ah=anthill2)
    ant4 = flexmock(x_loc = 9, y_loc = 9, owner = enemy, width=ant_width, height=ant_width, from_ah= anthill2, to_ah=anthill1)
    ant5 = flexmock(x_loc = 41, y_loc = 41, owner = enemy, width=ant_width, height=ant_width, from_ah= anthill2, to_ah=anthill1)
    ant6 = flexmock(x_loc = 22, y_loc = 22, owner = enemy, width=ant_width, height=ant_width, from_ah= anthill2, to_ah=anthill1)
    
    ants = [ant1, ant2, ant3]
    map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(map)
    assert(colliding_ant == set())

    ants = [ant4]
    map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(map)
    assert(colliding_ant == set(ant4))
    
    ants = [ant3, ant6]
    map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(map)
    assert(colliding_ant == set((ant3, ant6)))

    ants = [ant5, ant6]
    map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}
    colliding_ant = __get_colliding_ants(map)
    assert(colliding_ant == set())

def test___choose_source():

    anthill1 = flexmock(owner=None, population=20, available=15)
    anthill1.get_population = lambda only_available: anthill1.available
    anthill2 = flexmock(owner=None, population=20, available=20)
    anthill2.get_population = lambda only_available: anthill2.available
    anthill3 = flexmock(owner=None, population=30, available=10)
    anthill3.get_population = lambda only_available: anthill3.available

    source, _, _ = __choose_source([anthill1, anthill2, anthill3])
    assert(source == anthill2)

def test___choose_target():
    map = flexmock()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy1 = flexmock(name='Monika', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy2 = flexmock(name='Alzbeta', lost_ah=lambda: None, gained_ah=lambda: None)

    anthill1 = flexmock(owner=owner, population=20, available=20)
    anthill1.get_population = lambda only_available = False : anthill1.available if only_available else anthill1.population
    anthill4 = flexmock(owner=owner, population=10, available=10)
    anthill4.get_population = lambda only_available = False: anthill4.available if only_available else anthill4.population

    anthill2 = flexmock(owner=enemy1, population=20, available=20)
    anthill2.get_population = lambda only_available = False: anthill2.available if only_available else anthill2.population

    anthill3 = flexmock(owner=enemy2, population=30, available=5)
    anthill3.get_population = lambda only_available = False: anthill3.available if only_available else anthill3.population
    anthill5 = flexmock(owner=enemy2, population=10, available=8)
    anthill5.get_population = lambda only_available = False: anthill5.available if only_available else anthill5.population

    anthills = [anthill1, anthill2, anthill3, anthill4, anthill5]

    map.player_ahs = {}
    for ah in anthills:
        if ah.owner in map.player_ahs:
            map.player_ahs[ah.owner].append(ah)
        else:
            map.player_ahs[ah.owner] = [ah]

    source, _, min_i = __choose_source(map.player_ahs[owner])
    # attack weakest enemyx
    to_ah = __choose_target(map.player_ahs[owner], [owner, enemy1, enemy2], source, owner, min_i, map)
    assert(to_ah == anthill2)
    anthill4.population = 3
    anthill4.available = 3
    # help low health anthill
    to_ah = __choose_target(map.player_ahs[owner], [owner, enemy1, enemy2], source, owner, min_i, map)
    assert(to_ah == anthill4)

    anthill1.population = 3
    anthill1.available = 3

    source, _, min_i = __choose_source(map.player_ahs[owner])
    # low health, dont attack
    to_ah = __choose_target(map.player_ahs[owner], [owner, enemy1, enemy2], source, owner, min_i, map)
    assert(to_ah == None)

def test___choose_target_no_ah():
    map = flexmock()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy1 = flexmock(name='Monika', lost_ah=lambda: None, gained_ah=lambda: None)

    anthill1 = flexmock(owner=owner, population=20, available=20)
    anthill1.get_population = lambda only_available = False : anthill1.available if only_available else anthill1.population
    anthill2 = flexmock(owner=owner, population=10, available=10)
    anthill2.get_population = lambda only_available = False: anthill2.available if only_available else anthill2.population

    map.player_ahs = {owner: [anthill1, anthill2], enemy1: []}

    source, _, min_i = __choose_source(map.player_ahs[owner])
    # attack weakest enemyx
    to_ah = __choose_target(map.player_ahs[owner], [owner, enemy1], source, owner, min_i, map)
    assert(to_ah == None)


def test___enemy_info():
    map = flexmock()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy1 = flexmock(name='Monika', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy2 = flexmock(name='Alzbeta', lost_ah=lambda: None, gained_ah=lambda: None)

    anthill1 = flexmock(owner=owner, population=20, available=20)
    anthill1.get_population = lambda: anthill1.population
    anthill4 = flexmock(owner=owner, population=10, available=10)
    anthill4.get_population = lambda: anthill4.population

    anthill2 = flexmock(owner=enemy1, population=20, available=20)
    anthill2.get_population = lambda: anthill2.population

    anthill3 = flexmock(owner=enemy2, population=30, available=5)
    anthill3.get_population = lambda: anthill3.population
    anthill5 = flexmock(owner=enemy2, population=10, available=8)
    anthill5.get_population = lambda: anthill5.population

    anthills = [anthill1, anthill2, anthill3, anthill4, anthill5]
    map.player_ahs = {}
    for ah in anthills:
        if ah.owner in map.player_ahs:
            map.player_ahs[ah.owner].append(ah)
        else:
            map.player_ahs[ah.owner] = [ah]


    sums, mins = __enemy_info([owner, enemy1, enemy2], owner, map)
    assert(len(sums) == 3)
    assert(len(mins) == 3)
    assert(sums[0] == float('inf'))
    assert(mins[0] == float('inf'))
    assert(sums[1] == 20)
    assert(map.player_ahs[enemy1][mins[1]] == anthill2)
    assert(sums[2] == 40)
    assert(map.player_ahs[enemy2][mins[2]] == anthill5)
