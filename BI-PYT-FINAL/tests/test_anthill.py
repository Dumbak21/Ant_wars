import pytest
from flexmock import flexmock
from model.anthill import Anthill

@pytest.mark.parametrize('available', [0, *range(7,14)])
def test_send_ants(available):
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    target_owner = flexmock(name='Petr', lost_ah=lambda: None, gained_ah=lambda: None)
    anthill = Anthill(owner, 20, available)
    target = Anthill(target_owner)

    send_cnt = 10
    actually_send_cnt = anthill.send_ants(send_cnt, target)

    assert(anthill.queue_to_send[target] == actually_send_cnt)
    if available >= send_cnt:
        assert(actually_send_cnt == send_cnt)
    else:
        assert(actually_send_cnt == available)

def test_update():
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy1 = flexmock(name='Marek', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy2 = flexmock(name='Marcel', lost_ah=lambda: None, gained_ah=lambda: None)
    enemy1_anthill = Anthill(enemy1, 20, 20)
    enemy2_anthill = Anthill(enemy2, 20, 20)

    pop = 20
    en1_cnt = 4
    en2_cnt = 2

    anthill = Anthill(owner, 20, 14, {enemy1_anthill : en1_cnt, enemy2_anthill : en2_cnt})


    for i in range(5):
        attacking_enemies = anthill.update()
        if i <= 1:
            assert(attacking_enemies == [enemy1_anthill, enemy2_anthill])
            en1_cnt -= 1
            assert(anthill.queue_to_send[enemy1_anthill] == en1_cnt)
            en2_cnt -= 1
            assert(anthill.queue_to_send[enemy2_anthill] == en2_cnt)
            pop -= 2
            assert(anthill.population == pop)
        elif i <= 3:
            assert(attacking_enemies == [enemy1_anthill])
            en1_cnt -= 1
            assert(anthill.queue_to_send[enemy1_anthill] == en1_cnt)
            pop -= 1
            assert(anthill.population == pop)
        else:
            assert(anthill.queue_to_send[enemy1_anthill] == 0)
            assert(anthill.queue_to_send[enemy2_anthill] == 0)

            assert(attacking_enemies == [])
            assert(anthill.population == 14)

def test_change_owner_none():
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    anthill = Anthill(owner)
    anthill.change_owner(None)

    assert(anthill.owner == None)

def test_change_owner():
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    new_owner = flexmock(name='Petr', lost_ah=lambda: None, gained_ah=lambda: None)
    anthill = Anthill(owner)
    anthill.change_owner(new_owner)

    assert(anthill.owner == new_owner)

@pytest.mark.parametrize('pop', [None, *range(0,10,2)])
def test_get_population(pop):
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    avail_pop = 10
    if pop is None:
        anthill = Anthill(owner, available_ants=avail_pop)
        assert(anthill.get_population(False) == 0)

    else:
        anthill = Anthill(owner, pop, avail_pop)
        assert(anthill.get_population(False) == pop)

@pytest.mark.parametrize('avail_pop', [None, *range(0,10,2)])
def test_get_population_available(avail_pop):
    owner = flexmock(name='Karel', lost_ah=lambda: None, gained_ah=lambda: None)
    pop = avail_pop
    if avail_pop is None:
        anthill = Anthill(owner, population=pop)
        assert(anthill.get_population(True) == 0)

    else:
        anthill = Anthill(owner, pop, avail_pop)
        assert(anthill.get_population(True) == avail_pop)
