'''
Manages GUI, draws objects on screen
'''

import pygame
from GUI.button_manager import play_game_btn, exit_btn, exit_game_btn
from model.gameState import GameState
from model.map import Map
from model.anthill import Anthill
from model.ant import Ant
from model.color import Color

ANT_CNT_FONT = pygame.font.SysFont('comicsans', 15)
ANNOUNCE_FONT = pygame.font.SysFont('Comic Sans MS', 40)

ANT_SIZE = 6
ANTHILL_SIZE = 50

MAP_AREA_SIZE = 300

def draw_button(WIN, button, x_loc, y_loc, res_state):
    '''Draws button with assigned result_state to return on push'''
    mouse_pos = pygame.mouse.get_pos()

    button.set_coords(x_loc, y_loc)
    if button.rect.collidepoint(mouse_pos):
        btn_area = button.draw_btn(WIN=WIN, scale=1.1)
        button.focused = True
        if pygame.mouse.get_pressed()[0] == 1:
            return res_state, btn_area
    else:
        button.focused = False
        btn_area = button.draw_btn(WIN=WIN)
    return None, btn_area

def draw_menu(WIN):
    '''Draws menu screen'''
    WIN.fill(Color.BG.value)

    screen_w, screen_h = pygame.display.get_surface().get_size()

    # PLAY BTN
    res,_ = draw_button(WIN, play_game_btn, screen_w//2 - play_game_btn.width//2,\
                            screen_h//3 - play_game_btn.height//2, GameState.PLAY)
    if res is not None:
        return res
    # EXIT BTN
    res,_ = draw_button(WIN, exit_btn, screen_w//2 - play_game_btn.width//2,\
                        (screen_h//3)*2 - exit_btn.height//2, GameState.EXIT)
    if res is not None:
        return res

    pygame.display.update()
    return None

def draw_anthill(WIN, x_loc, y_loc, anthill : Anthill, map : Map, scale = 1, ah_color = Color.GREEN, ah_selected = False) -> pygame.Rect:
    '''Draws anthill on map'''
    anthill.x_loc, anthill.y_loc = x_loc, y_loc
    anthill.height, anthill.width = ANTHILL_SIZE, ANTHILL_SIZE
    ah_area = pygame.Rect(x_loc, y_loc, ANTHILL_SIZE*scale, ANTHILL_SIZE*scale)
    pygame.draw.rect(WIN ,rect=ah_area, color=Color.AH_AREA_CLR.value)
    #if anthill.clicked and anthill.owner is None:    
    if ah_selected and anthill.owner == map.current_player:    
        pygame.draw.rect(WIN ,rect=ah_area, color=Color.BLACK.value, width=2)

    if anthill.population >= 100:
        ant_cnt = ANT_CNT_FONT.render('99', 1, Color.RED.value)
    elif anthill.population < 0:
        ant_cnt = ANT_CNT_FONT.render('0', 1, Color.RED.value)
    else:
        ant_cnt = ANT_CNT_FONT.render(str(anthill.population), 1, Color.BLACK.value)
    cnt_x = x_loc + (ANTHILL_SIZE*scale // 2) - (ant_cnt.get_width() // 2)
    cnt_y = y_loc + (ANTHILL_SIZE*scale // 2) - (ant_cnt.get_height() // 2)

    text_background = pygame.Rect( cnt_x, cnt_y, *ant_cnt.get_size())
    pygame.draw.rect(WIN ,rect=text_background, color=ah_color.value)

    WIN.blit(ant_cnt, (cnt_x, cnt_y))


    mouse_pos = pygame.mouse.get_pos()

    if ah_area.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0] == 1:
            if anthill.clicked is False:
                anthill.clicked = True
                return ah_area, True
    if pygame.mouse.get_pressed()[0] == 0:
        anthill.clicked = False

    return ah_area, False

def draw_ant(WIN, x_loc, y_loc, scale, color, ant : Ant, map : Map):
    '''Draws ant on map'''
    ant.height, ant.width = ANT_SIZE, ANT_SIZE
    if ant.x_loc is None:
        ant.x_loc = ant.from_ah.x_loc + (ant.from_ah.width // 2) - (ant.width // 2)
        ant.y_loc = ant.from_ah.y_loc + (ant.from_ah.height // 2) - (ant.height // 2)
        map.ant_coords[ant] = (ant.x_loc, ant.y_loc)
        x_loc, y_loc = ant.x_loc, ant.y_loc
    else:
        ant.x_loc, ant.y_loc = x_loc, y_loc
    ant_area = pygame.Rect(x_loc, y_loc, ANT_SIZE*scale, ANT_SIZE*scale)
    pygame.draw.rect(WIN ,rect=ant_area, color=color)
    pygame.draw.rect(WIN ,rect=ant_area, color=Color.BLACK.value, width=1)
    return ant_area

def draw_map(WIN, x_loc, y_loc, map : Map, play_state = None, scale = 1):
    '''Draws whole map on screen'''
    map_area = pygame.Surface((MAP_AREA_SIZE*scale,MAP_AREA_SIZE*scale))
    map_area.fill(Color.MAP_AREA_CLR.value)
    clicked_element = None
    result_state = None

    for ah, coords in map.ah_coords.items():
        ah_x,ah_y = coords
        if ah.owner == map.current_player:
            ah_color = Color.GREEN
        else:
            ah_color = map.player_colors[ah.owner]
        border = False
        if ah == map.selected_ah:
            border = True
        _, clicked = draw_anthill(map_area, ah_x, ah_y, ah, map, scale, ah_color, border)
        if clicked:
            # check for right player
            if play_state == GameState.SELECTING_AH:
                # if map.current_player == ah.owner: if more players
                if ah.owner == map.current_player:
                    clicked_element = ah
                    result_state = GameState.SELECTED_AH
            elif play_state == GameState.SELECTING_ENEMY:
                clicked_element = ah
                result_state = GameState.SELECTED_ENEMY
            # gui representation of clicked


    for ant, coords in map.ant_coords.items():
        ant_x, ant_y = coords
        if ant.owner == map.current_player:
            color = Color.GREEN
        else:
            if ant.owner in map.player_colors:
                color = map.player_colors[ant.owner]
            else:
                raise Exception('player has no assigned color')
        draw_ant(map_area, ant_x, ant_y, scale, color.value, ant, map)

    WIN.blit(map_area, (x_loc, y_loc))

    return result_state, clicked_element

def draw_game(WIN, map : Map, play_state = None):
    '''Draws whole playing screen with map and rest'''
    WIN.fill(Color.BG.value)
    screen_w, _ = pygame.display.get_surface().get_size()

    # EXIT BTN
    res, _ = draw_button(WIN, exit_game_btn, screen_w-exit_game_btn.width-5, 5, GameState.MENU)
    if res is not None:
        return res, None

    # GAME MAP
    result_state, clicked_element = draw_map(WIN, 10, 10, map, play_state)
    if result_state is not None:
        return result_state, clicked_element

    return None, None

def draw_win(WIN):
    '''Draws winner screen'''
    WIN.fill(Color.BG.value)

    screen_w, screen_h = pygame.display.get_surface().get_size()

    winner_text = ANNOUNCE_FONT.render('WINNER', False, Color.BLACK.value)

    WIN.blit(winner_text, (screen_w//2 - winner_text.get_width()//2,\
                        screen_h//2 - winner_text.get_height()//2))

def draw_loose(WIN):
    '''Draws looser screen'''
    WIN.fill(Color.BG.value)

    screen_w, screen_h = pygame.display.get_surface().get_size()

    looser_text = ANNOUNCE_FONT.render('LOOSER', False, Color.BLACK.value)

    WIN.blit(looser_text, (screen_w//2 - looser_text.get_width()//2,\
                        screen_h//2 - looser_text.get_height()//2))

def draw_next_round(WIN):
    '''Draws next round screen'''
    WIN.fill(Color.BG.value)

    screen_w, screen_h = pygame.display.get_surface().get_size()

    looser_text = ANNOUNCE_FONT.render('NEXT ROUND', False, Color.BLACK.value)

    WIN.blit(looser_text, (screen_w//2 - looser_text.get_width()//2,\
                        screen_h//2 - looser_text.get_height()//2))

def get_nickname():
    '''Return nickname of user (can be modified for screen with input)'''
    return 'ProudCTUstudent'
