import pytest
from model.player import Player

def test_name():
    '''
    name
    '''
    with pytest.raises(ValueError):
        Player(None)
    with pytest.raises(ValueError):
        Player("")
    with pytest.raises(TypeError):
        Player(666)

    name = "Karel"
    player = Player(name)
    assert player.get_name() == name


def test_ah_count():
    '''
    ah count
    '''
    with pytest.raises(ValueError):
        Player("Karel", -2)
    player = Player("Karel")
    assert player is not None
    assert player.get_ah_cnt() == 0
    player = Player("Jan", 5)
    assert player.get_ah_cnt() == 5

    player.reset()
    assert player.get_ah_cnt() == 0

def test_gain_loss():
    '''
    gain, loss
    '''
    player = Player("Karel")
    assert player.get_ah_cnt() == 0
    player.lost_ah()
    assert player.get_ah_cnt() == 0

    gain_cnt = 5

    for i in range(gain_cnt):
        player.gained_ah()
        assert player.get_ah_cnt() == i+1
    for i in range(gain_cnt + 1):
        player.lost_ah()
        assert player.get_ah_cnt() == max(0, gain_cnt - (i+1))

    assert player.get_ah_cnt() == 0
