import pytest
from flexmock import flexmock
from model.map import Map, get_new_ant_loc

def test_place_anthill():
    map = Map()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    anthill1 = flexmock(owner=owner, population=20, x_loc=0, y_loc=0)
    anthill2 = flexmock(owner=owner, population=20, x_loc=0, y_loc=0)

    map.place_anthill(anthill1, 10, 5)
    map.place_anthill(anthill2, 5, 20)

    assert(anthill1.x_loc == 10 and anthill1.y_loc == 5)
    assert(anthill2.x_loc == 5 and anthill2.y_loc == 20)

    assert(map.anthills == [anthill1, anthill2])
    assert(map.ah_coords[anthill1] == (10,5))
    assert(map.ah_coords[anthill2] == (5,20))
    assert(map.player_ahs[owner] == [anthill1, anthill2])


def test_ah_change_owner():
    map = Map()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    new_owner = flexmock(name='Diviš', lost_ah=lambda: None, gained_ah=lambda: None)
    anthill1 = flexmock(owner=owner, population=20, change_owner=lambda x: None)
    anthill2 = flexmock(owner=owner, population=20, change_owner=lambda x: None)

    map.place_anthill(anthill1, 10, 5)
    map.place_anthill(anthill2, 5, 20)

    map.ah_change_owner(anthill1, new_owner)

    assert(map.anthills == [anthill1, anthill2])
    assert(map.ah_coords[anthill1] == (10,5))
    assert(map.ah_coords[anthill2] == (5,20))

    assert(map.player_ahs[owner] == [anthill2])
    assert(map.player_ahs[new_owner] == [anthill1])

    assert(len(map.player_ahs) == 2)

def test_assign_empty_ahs():
    map = Map()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    new_owner = flexmock(name='Diviš', lost_ah=lambda: None, gained_ah=lambda: None)
    anthill1 = flexmock(owner=owner, population=20, change_owner=lambda x: None)
    anthill2 = flexmock(owner=None, population=20, change_owner=lambda x: None)

    map.place_anthill(anthill1, 10, 5)
    map.place_anthill(anthill2, 5, 20)

    map.assign_empty_ahs(new_owner)

    assert(map.player_ahs[new_owner] == [anthill2])
    assert(map.player_ahs[owner] == [anthill1])

def test___update_ants_loc():
    map = Map()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy = flexmock(name='Diviš', lost_ah=lambda: None, gained_ah=lambda: None)

    anthill1 = flexmock(owner=owner, population=20, width=10, height=10)
    anthill2 = flexmock(owner=enemy, population=20, width=10, height=10)

    map.place_anthill(anthill1, 10, 5)
    map.place_anthill(anthill2, 10, 100)

    ant_start_pos = 6
    ant_step_size = 10

    ant_width = 6

    ants = [ flexmock(from_ah = anthill1, to_ah = anthill2, owner=owner, x_loc=10 + anthill1.width//2 - ant_width//2, y_loc=ant_start_pos+ant_step_size*i, width=ant_width, height=ant_width) for i in range(5)]
    map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}

    map._Map__update_ants_loc(get_new_ant_loc, ant_step_size)

    for i, item in enumerate(map.ant_coords.items()):
        ant, coords = item
        _x, _y = coords

        assert(ant.x_loc == _x)
        assert(ant.y_loc == _y)
        assert(coords == (10 + anthill1.width//2 - ant.width//2, ant_start_pos + (i+1)*ant_step_size))


def test___get_ants_to_spawn():
    map = Map()
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy = flexmock(name='Diviš', lost_ah=lambda: None, gained_ah=lambda: None)

    anthill1 = flexmock(owner=owner, population=20, available=15, width=10, height=10)

    anthill2 = flexmock(owner=enemy, population=20, available=20, width=10, height=10)
    anthill3 = flexmock(owner=enemy, population=20, available=20, width=10, height=10)

    anthill1.update = lambda : [anthill2, anthill3]
    anthill2.update = lambda : []
    anthill3.update = lambda : []

    map.place_anthill(anthill1, 10, 5)
    map.place_anthill(anthill2, 10, 100)

    ants_to_spawn = map._Map__get_ants_to_spawn()

    assert(ants_to_spawn == [(anthill1, anthill2), (anthill1, anthill3)])


def test_get_new_ant_loc():
    map = Map()
    #anthill1 = flexmock(owner=None, population=20, available=15, width=10, height=10)
    anthill2 = flexmock(owner=None, population=20, available=20, width=10, height=10, x_loc=15, y_loc=35)
    map.ah_coords[anthill2] = 15, 35

    ant_width = 6
    ant = flexmock(to_ah=anthill2, width=ant_width, height=ant_width, x_loc=10, y_loc=10)

    map.ant_coords[ant] = (10, 10)
    step_size = 1

    for i in range(100):
        new_loc = get_new_ant_loc(ant, map, step_size)
        map.ant_coords[ant] = new_loc
        #print(new_loc)
        if new_loc == (anthill2.x_loc + anthill2.width//2 - ant_width//2, anthill2.y_loc + anthill2.height//2 - ant_width//2):
            assert(True)
            return
    assert(False)