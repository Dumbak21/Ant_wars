from enum import Enum

class GameState(Enum):
    '''Enum - states of game'''
    MENU = 1
    PLAY = 2
    EXIT = 3

    SELECTING_AH = 4
    SELECTED_AH = 5
    SELECTING_ENEMY = 6
    SELECTED_ENEMY = 7

    WIN = 8
    LOOSE = 9
