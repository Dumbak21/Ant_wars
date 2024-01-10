'''
AntWars-like game
'''

from random import randint
from GUI.gui_manager import draw_menu, get_nickname, draw_win, draw_loose, draw_next_round
from model.gameState import GameState
from utils import retrieve_map, assign_color_to_players
from model.player import Player
from game import game_round
import pygame


WIDTH, HEIGHT = 600, 350
FPS = 60
SPEED = 10
ANT_INC_SPEED = 150
BOT_PLAY_SPEED_MAX = 350
BOT_PLAY_SPEED_MIN = 120

FIRST_MAP_ID = 100

BLACK = (0,0,0)


def handle_win(win):
    '''Shows win screeen and returns new states and redirects to menu'''
    draw_win(win)
    pygame.display.update()
    pygame.time.wait(2000)
    current_screen = GameState.MENU
    current_state = GameState.SELECTING_AH
    return current_screen, current_state

def handle_loose(win):
    '''Shows next round screen and redirects to next map'''
    draw_loose(win)
    pygame.display.update()
    pygame.time.wait(2000)
    current_screen = GameState.MENU
    current_state = GameState.SELECTING_AH
    return current_screen, current_state

def handle_next_round(win):
    '''Shows loose screeen and returns new states and redirects to menu'''
    draw_next_round(win)
    pygame.display.update()
    pygame.time.wait(2000)
    current_screen = GameState.PLAY
    current_state = GameState.SELECTING_AH
    return current_screen, current_state

def set_new_map(player, ah_map):
    '''Sets new loaded map for use'''
    player.reset()
    ah_map.current_player = player
    ah_map.assign_empty_ahs(ah_map.current_player)
    player_colors = assign_color_to_players(ah_map.players)
    ah_map.player_colors = player_colors

    return ah_map

def get_map(map_id, player):
    '''Get set map'''
    ah_map = None
    ah_map = retrieve_map(map_id)
    if ah_map is None:
        raise Exception('Map does not exist')
    ah_map = set_new_map(player, ah_map)
    return ah_map

def try_get_next_map(map_id, player):
    '''Get next map'''
    ah_map = None
    try:
        ah_map = get_map(map_id+1, player)
    finally:
        return ah_map


def init_win():
    '''
    Initialize window
    '''
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption('AntWars 3.0')

    return win

def destr_game():
    pygame.quit()

def main_loop(win : pygame.display):
    '''
    By running this new window will popup and you will be able to play my game Antwars
    '''
    clock = pygame.time.Clock()
    game_loop = True

    # Map
    ah_map = None
    map_id = FIRST_MAP_ID

    # Player
    player = Player(get_nickname())
    current_screen = GameState.MENU
    current_state = GameState.SELECTING_AH
    # Timers
    speed_division_step = 0
    speed_division_inc = 0
    speed_division_simul = 0
    simul_interval = randint(BOT_PLAY_SPEED_MIN, BOT_PLAY_SPEED_MAX)

    while game_loop:
        clock.tick(FPS)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        # MENU
        if current_screen == GameState.MENU:
            new_screen = draw_menu(win)
            if new_screen is not None:
                if new_screen == GameState.PLAY:
                    # load map
                    ah_map = get_map(map_id, player)
                current_screen = new_screen

        # WIN
        if current_screen == GameState.WIN:
            new_map = try_get_next_map(map_id, player)
            if new_map is None:
                current_screen, current_state = handle_win(win)
                map_id = FIRST_MAP_ID
            else:
                current_screen, current_state = handle_next_round(win)
                map_id += 1
                ah_map = new_map

        # LOOSE
        if current_screen == GameState.LOOSE:
            current_screen, current_state = handle_loose(win)
            map_id = FIRST_MAP_ID

        # PLAY clicked
        if current_screen == GameState.PLAY:
            update_ah_cnt = False
            update_ant_step = False
            simulate = False

            # Steps
            if speed_division_step % SPEED == 0:
                update_ant_step = True
                speed_division_step = 0
            speed_division_step += 1

            # AH inc
            if speed_division_inc % ANT_INC_SPEED == 0:
                update_ah_cnt = True
                speed_division_inc = 0
            speed_division_inc += 1

            # Simulate attack
            if speed_division_simul >= simul_interval:
                simulate = True
                speed_division_simul = 0
                simul_interval = randint(BOT_PLAY_SPEED_MIN, BOT_PLAY_SPEED_MAX)
            speed_division_simul += 1

            result_sreen, result_state = game_round(win, ah_map, current_state,\
                                            update_ant_step, update_ah_cnt, simulate)

            if result_sreen is not None:
                current_screen = result_sreen
                current_state = GameState.SELECTING_AH
                if result_sreen != GameState.WIN:
                    map_id = FIRST_MAP_ID
            if result_state is not None:
                current_state = result_state

        # EXIT clicked
        if current_screen == GameState.EXIT:
            game_loop = False

        pygame.display.update()
    pygame.display.quit()

if __name__ == '__main__':
    game_win = init_win()
    main_loop(game_win)
    destr_game()
