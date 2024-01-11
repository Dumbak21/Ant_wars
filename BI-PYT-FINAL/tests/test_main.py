'''main tests'''

import pytest
from flexmock import flexmock

import GUI.gui_manager as gui_modul
from main import init_win, set_new_map
import main


def test_set_map():
    player = flexmock(reset=lambda:None)
    enemy = flexmock(reset=lambda:None)
    ah_map = flexmock(players=[enemy])
    ah_map.should_receive('assign_empty_ahs').once()

    new_map = set_new_map(player, ah_map)

    assert new_map.current_player == player
    assert len(new_map.player_colors) > 0

    