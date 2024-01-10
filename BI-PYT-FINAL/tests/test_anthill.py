import pytest
from model.anthill import Anthill
from model.player import Player

# FIXTURES

@pytest.fixture
def players():
    '''
    return players (first is owner)
    '''
    return [Player('Karel'), Player('Lucka'), Player('Marek')]
    #return flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)

@pytest.fixture
def owner_player_anthill(players):
    '''
    return players anthill
    '''
    return Anthill(players[0])


# TESTS


def test_change_owner_none(owner_player_anthill):
    '''
    no owner
    '''
    owner = owner_player_anthill.owner
    owner_ah_cnt = owner_player_anthill.owner.number_of_ahs

    owner_player_anthill.change_owner(None)

    assert owner_player_anthill.owner is None
    assert owner.number_of_ahs == owner_ah_cnt-1


def test_change_owner(players):
    '''
    new owner
    '''
    owner_player_anthill = Anthill(players[0])
    owner_ah_cnt = players[0].number_of_ahs
    new_owner_ah_cnt = players[1].number_of_ahs
    owner_player_anthill.change_owner(players[1])
    assert owner_player_anthill.owner == players[1]
    assert players[0].number_of_ahs == owner_ah_cnt - 1
    assert players[1].number_of_ahs == new_owner_ah_cnt + 1

@pytest.mark.parametrize('pop', [*range(0,10,2)])
def test_population(pop, players):
    '''
    anthill population set/get
    '''
    owner_player = players[0]
    avail_pop = 5
    if pop >= avail_pop:
        anthill = Anthill(owner_player, population=pop, available_ants=avail_pop)
        assert anthill.get_population(False) == pop
        assert anthill.get_population(True) == avail_pop
    else:
        with pytest.raises(ValueError):
            Anthill(owner_player, population=pop, available_ants=avail_pop)


@pytest.mark.parametrize('pop', [*range(0,10,2)])
def test_inc(pop, players):
    '''
    anthill population inc
    '''
    owner_player = players[0]
    avail_pop = max(0, pop - 2)
    anthill = Anthill(owner_player, population=pop, available_ants=avail_pop)
    
    anthill.inc()

    assert anthill.get_population(False) == pop + 1
    assert anthill.get_population(True) == avail_pop + 1


@pytest.mark.parametrize('pop, cnt', [*zip([*range(0,10,2)], [*range(-3,3,1)])])
def test_accept_ants(pop, cnt, players):
    '''
    accepting new ants
    '''
    owner_player = players[0]
    avail_pop = max(0, pop - 1)
    anthill = Anthill(owner_player, population=pop, available_ants=avail_pop)

    if cnt < 0:
        with pytest.raises(ValueError):
            anthill.accept_ants(cnt)
        assert anthill.get_population(False) == pop
        assert anthill.get_population(True) == avail_pop
    else:
        anthill.accept_ants(cnt)
        assert anthill.get_population(False) == pop + cnt
        assert anthill.get_population(True) == avail_pop + cnt

@pytest.mark.parametrize('pop, cnt', [*zip([*range(0,10,2)], [*range(-3,3,1)])])
def test_kill_ants(pop, cnt, players):
    '''
    accepting new ants
    '''
    owner_player = players[0]
    avail_pop = max(0, pop - 1)
    anthill = Anthill(owner_player, population=pop, available_ants=avail_pop)

    if cnt < 0:
        with pytest.raises(ValueError):
            anthill.kill_ants(cnt)
        assert anthill.get_population(False) == pop
        assert anthill.get_population(True) == avail_pop
    else:
        res = anthill.kill_ants(cnt)
        if cnt > pop:
            # all killed
            assert anthill.get_population(False) == abs(pop - cnt)
            assert anthill.get_population(True) == abs(pop - cnt)
            assert isinstance(anthill.get_queue_to_send(), dict)
            assert len(anthill.get_queue_to_send()) == 0
            assert res is True
        else:
            assert anthill.get_population(False) == pop - cnt
            assert anthill.get_population(True) == avail_pop - cnt
            assert res is False


@pytest.mark.parametrize('available, send_cnt', [*zip([0,4, *range(7,14)], [*range(-4,14,2)])])
def test_send_ants(available, send_cnt, players):
    '''
    sending and send queue
    '''
    pop = 20
    anthill = Anthill(players[0], pop, available)
    target = Anthill(players[0])
    assert isinstance(anthill.get_queue_to_send(), dict)
    assert len(anthill.get_queue_to_send()) == 0

    if send_cnt < 0:
        with pytest.raises(ValueError):
            anthill.send_ants(send_cnt, target)
        assert len(anthill.get_queue_to_send()) == 0
        return
    
    actually_send_cnt = anthill.send_ants(send_cnt, target)
    if send_cnt > available:
        assert actually_send_cnt == available
    else:
        assert actually_send_cnt == send_cnt

    assert len(anthill.get_queue_to_send()) == 1
    assert anthill.get_queue_to_send()[target] == actually_send_cnt


    actually_send_cnt_rem = anthill.send_ants(send_cnt, target)
    assert len(anthill.get_queue_to_send()) == 1
    assert anthill.get_queue_to_send()[target] == actually_send_cnt + actually_send_cnt_rem


@pytest.mark.run('last')
def test_update(players):
    '''
    test round sending ants
    '''
    enemy1_anthill = Anthill(players[1], 20, 20)
    enemy2_anthill = Anthill(players[2], 20, 20)

    pop = 20
    en1_cnt = 4
    en2_cnt = 2
    avail_pop = pop-en1_cnt-en2_cnt
    anthill = Anthill(players[0], population=pop, available_ants=avail_pop ,\
                    queue_to_send={enemy1_anthill : en1_cnt, enemy2_anthill : en2_cnt})


    for i in range(6):
        attacking_enemies = anthill.update()
        if i <= 1:                          # Attacking both AHs
            assert len(attacking_enemies) == 2
            assert set(attacking_enemies) == set([enemy1_anthill, enemy2_anthill])
            en1_cnt -= 1
            en2_cnt -= 1
            assert anthill.get_queue_to_send()[enemy1_anthill] == en1_cnt
            assert anthill.get_queue_to_send()[enemy2_anthill] == en2_cnt
            pop -= 2
        elif i <= 3:                        # Attacking one AH
            assert len(attacking_enemies) == 1
            assert attacking_enemies == [enemy1_anthill]
            en1_cnt -= 1
            assert anthill.queue_to_send[enemy1_anthill] == en1_cnt
            pop -= 1
        else:
            assert len(attacking_enemies) == 0
            assert enemy1_anthill not in anthill.get_queue_to_send().keys() or\
                    anthill.queue_to_send[enemy1_anthill] == 0
            assert enemy1_anthill not in anthill.get_queue_to_send().keys() or\
                    anthill.queue_to_send[enemy2_anthill] == 0

        assert anthill.get_population(False) == pop
        assert anthill.get_population(True) == avail_pop
