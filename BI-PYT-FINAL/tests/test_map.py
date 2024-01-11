'''Map tests'''

import pytest
from flexmock import flexmock
from model.map import Map, get_new_ant_loc, ANTHILL_SIZE, MAP_AREA_SIZE
from model.player import Player
from model.anthill import Anthill
# FIXTURES

@pytest.fixture
def players():
    '''
    return players (first is owner)
    '''
    return [Player('Karel'), Player('Lucka'), Player('Marek')]

# TEST

@pytest.mark.parametrize('x_loc, y_loc', [*zip([*range(-ANTHILL_SIZE-2,ANTHILL_SIZE+2,3), \
                                                *range(MAP_AREA_SIZE-ANTHILL_SIZE-2,MAP_AREA_SIZE+ANTHILL_SIZE+2,3)],\
                                                [*range(-ANTHILL_SIZE-2,ANTHILL_SIZE+2,3), \
                                                *range(MAP_AREA_SIZE-ANTHILL_SIZE-2,MAP_AREA_SIZE+ANTHILL_SIZE+2,3)]
                                                )])
def test_place_anthill_loc(x_loc, y_loc, players):
    '''bad loc ahs'''
    ah_map = Map()
    owner = players[0]
    anthill1 = Anthill(owner, 20, 20)

    if x_loc < 0 or y_loc < 0 or\
       x_loc > MAP_AREA_SIZE - ANTHILL_SIZE //2 or y_loc > MAP_AREA_SIZE - ANTHILL_SIZE // 2:
        with pytest.raises(ValueError):
            ah_map.place_anthill(anthill1, x_loc, y_loc)
        assert anthill1.x_loc is None and anthill1.y_loc is None
        assert len(ah_map.anthills) == 0
        assert anthill1 not in ah_map.ah_coords
        assert owner not in ah_map.player_ahs
    else:
        ah_map.place_anthill(anthill1, x_loc, y_loc)
        assert anthill1.x_loc == x_loc and anthill1.y_loc == y_loc
        assert len(ah_map.anthills) == 1
        assert anthill1 in ah_map.ah_coords
        assert owner in ah_map.player_ahs
        assert anthill1 in ah_map.player_ahs[owner]

@pytest.mark.run(after='test_place_anthill_loc')
@pytest.mark.parametrize('x_loc, y_loc', [*zip([*range(MAP_AREA_SIZE//2-ANTHILL_SIZE-2,MAP_AREA_SIZE//2+ANTHILL_SIZE+2,3)],
                                                [*range(MAP_AREA_SIZE//2-ANTHILL_SIZE-2,MAP_AREA_SIZE//2+ANTHILL_SIZE+2,3)], 
                                                )])
def test_place_anthill_collide(x_loc, y_loc, players):
    '''collide ahs'''
    ah_map = Map()
    owner = players[0]
    anthill1 = Anthill(owner, 20, 20)
    anthill2 = Anthill(owner, 20, 20)

    ah_map.place_anthill(anthill1, MAP_AREA_SIZE//2, MAP_AREA_SIZE//2)
    if x_loc >= anthill1.x_loc - ANTHILL_SIZE - 1 and x_loc < anthill1.x_loc + ANTHILL_SIZE + 1 and\
       y_loc >= anthill1.y_loc - ANTHILL_SIZE - 1 and y_loc < anthill1.y_loc + ANTHILL_SIZE + 1:
        with pytest.raises(ValueError):
            ah_map.place_anthill(anthill2, x_loc, y_loc)

        assert anthill2.x_loc is None and anthill2.y_loc is None
        assert ah_map.anthills == [anthill1]
        assert anthill1 in ah_map.ah_coords
        assert ah_map.ah_coords[anthill1] == (MAP_AREA_SIZE//2, MAP_AREA_SIZE//2)
        assert anthill2 not in ah_map.ah_coords
        assert ah_map.player_ahs[owner] == [anthill1]
    else:
        ah_map.place_anthill(anthill2, x_loc, y_loc)
        assert anthill2.x_loc == x_loc and anthill2.y_loc == y_loc
        assert set(ah_map.anthills) == set([anthill1, anthill2])
        assert anthill1 in ah_map.ah_coords
        assert anthill2 in ah_map.ah_coords
        assert ah_map.ah_coords[anthill1] == (MAP_AREA_SIZE//2, MAP_AREA_SIZE//2)
        assert ah_map.ah_coords[anthill2] == (x_loc, y_loc)
        assert set(ah_map.player_ahs[owner]) == set([anthill1, anthill2])


def test_ah_change_owner(players):
    '''change owner'''
    ah_map = Map()
    owner = players[0]
    new_owner = players[1]
    anthill1 = Anthill(owner, 20, 20)
    anthill2 = Anthill(owner, 20, 20)

    ah_map.place_anthill(anthill1, 10, 5)
    ah_map.place_anthill(anthill2, 10 + ANTHILL_SIZE + 5, 5 + ANTHILL_SIZE + 5)

    assert owner.get_ah_cnt() == 2
    assert new_owner.get_ah_cnt() == 0

    ah_map.ah_change_owner(anthill1, new_owner)

    assert owner.get_ah_cnt() == 1
    assert new_owner.get_ah_cnt() == 1

    assert set(ah_map.anthills) == set([anthill1, anthill2])
    assert anthill1 in ah_map.ah_coords
    assert anthill2 in ah_map.ah_coords

    assert owner in ah_map.player_ahs
    assert ah_map.player_ahs[owner] == [anthill2]
    assert new_owner in ah_map.player_ahs
    assert ah_map.player_ahs[new_owner] == [anthill1]
    assert len(ah_map.player_ahs) == 2


def test_inc_all_ahs(players):
    '''
    inc pop in all ahs
    '''
    ah_map = Map()
    owner = players[0]
    new_owner = players[1]
    anthill1 = flexmock(owner=owner)
    anthill1.should_receive("inc").once()
    anthill2 = flexmock(owner=new_owner)
    anthill2.should_receive("inc").once()

    ah_map.place_anthill(anthill1, 10, 5)
    ah_map.place_anthill(anthill2, 10 + ANTHILL_SIZE + 5, 5 + ANTHILL_SIZE + 5)

    ah_map.inc_anthills()


def test_assign_empty_ahs(players):
    '''Assign empty ahs'''
    ah_map = Map()

    owner = players[0]
    new_owner = players[1]
    anthill1 = Anthill(owner, 20, 20)
    anthill2 = Anthill(None, 20, 20)

    ah_map.place_anthill(anthill1, 10, 5)
    ah_map.place_anthill(anthill2, 10 + ANTHILL_SIZE + 5, 5 + ANTHILL_SIZE + 5)

    ah_map.assign_empty_ahs(new_owner)

    assert set(ah_map.anthills) == set([anthill1, anthill2])
    assert ah_map.player_ahs[new_owner] == [anthill2]
    assert ah_map.player_ahs[owner] == [anthill1]


def test_send_ants(players):
    '''send ants'''
    ah_map = Map()
    count = 5
    owner = players[0]
    enemy = players[2]
    anthill1 = Anthill(owner, 20, 20)
    anthill2 = Anthill(enemy, 20, 20)
    anthill1 = flexmock(anthill1)
    anthill1.should_call('send_ants').with_args(count=count, to_ah=anthill2).once()

    ah_map.send_ants(anthill1, anthill2, count)



def test_get_new_ant_loc():
    '''Test that new ant loc (somehow) leads to end'''
    ah_map = Map()
    anthill2 = flexmock(owner=None, population=20, available=20, width=10, height=10, x_loc=15, y_loc=35)
    ah_map.ah_coords[anthill2] = 15, 35

    ant_width = 6
    ant = flexmock(to_ah=anthill2, width=ant_width, height=ant_width, x_loc=10, y_loc=10)

    ah_map.ant_coords[ant] = (10, 10)
    step_size = 1

    for _ in range(100):
        new_loc = get_new_ant_loc(ant, ah_map, step_size)
        ah_map.ant_coords[ant] = new_loc
        if new_loc == (anthill2.x_loc + anthill2.width//2 - ant_width//2, anthill2.y_loc + anthill2.height//2 - ant_width//2):
            assert True
            return
    assert False



# PRIVATE METHODS

# def test___update_ants_loc(players):
#     ah_map = Map()
#     owner = players[0]
#     enemy = players[1]

#     anthill1 = flexmock(owner=owner, population=20, width=10, height=10)
#     anthill2 = flexmock(owner=enemy, population=20, width=10, height=10)

#     ah_map.place_anthill(anthill1, 10, 5)
#     ah_map.place_anthill(anthill2, 10, 100)

#     ant_start_pos = 6
#     ant_step_size = 10

#     ant_width = 6

#     ants = [ flexmock(from_ah = anthill1, to_ah = anthill2, owner=owner, x_loc=10 + anthill1.width//2 - ant_width//2, y_loc=ant_start_pos+ant_step_size*i, width=ant_width, height=ant_width) for i in range(5)]
#     ah_map.ant_coords = { ant : (ant.x_loc, ant.y_loc) for ant in ants}

#     ah_map._Map__update_ants_loc(get_new_ant_loc, ant_step_size)

#     for i, item in enumerate(ah_map.ant_coords.items()):
#         ant, coords = item
#         _x, _y = coords

#         assert(ant.x_loc == _x)
#         assert(ant.y_loc == _y)
#         assert(coords == (10 + anthill1.width//2 - ant.width//2, ant_start_pos + (i+1)*ant_step_size))


# def test___get_ants_to_spawn():
#     ah_map = Map()
#     owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
#     enemy = flexmock(name='Diviš', lost_ah=lambda: None, gained_ah=lambda: None)

#     anthill1 = flexmock(owner=owner, population=20, available=15, width=10, height=10)

#     anthill2 = flexmock(owner=enemy, population=20, available=20, width=10, height=10)
#     anthill3 = flexmock(owner=enemy, population=20, available=20, width=10, height=10)

#     anthill1.update = lambda : [anthill2, anthill3]
#     anthill2.update = lambda : []
#     anthill3.update = lambda : []

#     ah_map.place_anthill(anthill1, 10, 5)
#     ah_map.place_anthill(anthill2, 10, 100)

#     ants_to_spawn = ah_map._Map__get_ants_to_spawn()

#     assert(ants_to_spawn == [(anthill1, anthill2), (anthill1, anthill3)])