'''
Takes care of each round on map, simulates bots
'''

from random import randint
from GUI.gui_manager import draw_game
from model.gameState import GameState
from model.map import Map
import pygame
import numpy as np
#import operator

def __serve_actions(new_state, target, ah_map):
    current_state = None
    if new_state is not None:
        if new_state == GameState.MENU:
            # Game exited
            return new_state, None
        if new_state == GameState.SELECTED_AH:
            selected_ah_from = target
            ah_map.selected_ah = selected_ah_from
            current_state = GameState.SELECTING_ENEMY
        if new_state == GameState.SELECTED_ENEMY:
            # Send ants
            selected_ah_to = target
            selected_ah_from = ah_map.selected_ah
            ah_map.selected_ah = None
            if selected_ah_from != selected_ah_to:
                ah_map.send_ants(selected_ah_from, selected_ah_to)
            current_state = GameState.SELECTING_AH
    return None, current_state

def __is_win_loose(ah_map : Map):
    if ah_map.current_player.get_ah_cnt() == ah_map.get_ah_cnt():
        for ant in ah_map.ant_coords.keys():
            if ant.owner != ah_map.current_player:
                return None
        return GameState.WIN
    if ah_map.current_player.get_ah_cnt() == 0:
        for ant in ah_map.ant_coords.keys():
            if ant.owner == ah_map.current_player:
                return None
        return GameState.LOOSE
    return None

def __get_colliding_ants(ah_map) -> set:
    ants_to_pop = set()
    for ant, _ in ah_map.ant_coords.items():
        ant_area = pygame.Rect(ant.x_loc, ant.y_loc, ant.width, ant.height)
        # Anthill collisions
        for ah, _ in ah_map.ah_coords.items():
            ah_area = pygame.Rect(ah.x_loc, ah.y_loc, ah.width, ah.height)
            if ah_area.colliderect(ant_area):
                if ah.owner == ant.owner:
                    if ah != ant.from_ah:
                        ah.accept_ants(1)
                        ants_to_pop.add(ant)
                else:
                    did_change_ownership = ah.kill_ants(1)
                    ants_to_pop.add(ant)
                    if did_change_ownership:
                        ah_map.ah_change_owner(ah, ant.owner)
        # Enemy ant collisions
        for enemy_ant, _ in ah_map.ant_coords.items():
            if ant != enemy_ant and ant.owner != enemy_ant.owner:
                enemy_ant_area = pygame.Rect(enemy_ant.x_loc, enemy_ant.y_loc,\
                                            enemy_ant.width, enemy_ant.height)
                if ant_area.colliderect(enemy_ant_area):
                    ants_to_pop.add(ant)
                    ants_to_pop.add(enemy_ant)
    return ants_to_pop


def game_round(win, ah_map : Map, current_state, update_ant_pos = False,\
                 update_ah_count = False, simulate_players_flag = False):
    '''Makes one round of game (draws, updates, increments, kills)'''
    # Draw game and get game actions/events
    new_state, target = draw_game(win, ah_map, current_state)

    # Take care of actions in game (pressed buttons/anthils)
    new_screen, new_state = __serve_actions(new_state, target, ah_map)
    if new_screen is not None:
        return new_screen, None
    if new_state is not None:
        current_state = new_state

    # for each ant collide with ants or ahs
    ants_to_pop = __get_colliding_ants(ah_map)

    # Remove dead ants
    for ant in ants_to_pop:
        if ant in ah_map.ant_coords:
            ah_map.ant_coords.pop(ant)

    # WIN / LOOSE
    new_state = __is_win_loose(ah_map)
    if new_state is not None:
        return new_state, None

    # Update ant pos
    if update_ant_pos:
        ah_map.update()
    # INC anthills population
    if update_ah_count:
        ah_map.inc_anthills()
    # Simulate bots
    if simulate_players_flag:
        player_for_simulation = ah_map.players
        player_for_simulation.append(ah_map.current_player)
        simulate_players(player_for_simulation, ah_map, simulate_player=False)
    # Continue game
    return None, current_state

CRITICAL_POPULATION = 6
CHANCE_OF_PLAYING = 75

def __choose_source(players_ahs):
    max_i = 0
    max_pop = 0
    min_i = 0
    min_pop = float('inf')

    for i, ah in enumerate(players_ahs):
        ah_pop = ah.get_population(only_available=True) 
        if ah_pop > max_pop:
            max_i = i
            max_pop = ah_pop

        if ah_pop < min_pop:
            min_i = i
            min_pop = ah_pop

    from_ah = players_ahs[max_i]

    return from_ah, max_i, min_i

def __enemy_info(players_for_simulation, player, ah_map):
    enemy_sums = [0] * len(players_for_simulation)
    enemy_mins = [0] * len(players_for_simulation)
    for i, enemy in enumerate(players_for_simulation):
        if enemy == player:
            enemy_sums[i] = float('inf')
            enemy_mins[i] = float('inf')
            continue
        enemy_ahs = ah_map.player_ahs[enemy]
        if len(enemy_ahs) == 0:
            enemy_sums[i] = float('inf')
            enemy_mins[i] = float('inf')
            continue

        ant_sum = 0    # How many ants does enemy have

        min_i = 0      # Weakest one
        min_pop = float('inf')

        for j, ah in enumerate(enemy_ahs):
            ah_pop = ah.get_population()
            ant_sum += ah_pop

            if ah_pop < min_pop:
                min_i = j
                min_pop = ah_pop

        enemy_sums[i] = ant_sum
        enemy_mins[i] = min_i
    return enemy_sums, enemy_mins

def __choose_target(players_ahs, players_for_simulation, from_ah, player, min_i, ah_map):
    # HEAL MY AH
    if players_ahs[min_i].get_population() < CRITICAL_POPULATION:   # My target
        if players_ahs[min_i] != from_ah:
            to_ah = players_ahs[min_i]
            return to_ah
        else:
            return None

    # Enemy target
    # Get info about enemy
    enemy_sums, enemy_mins = __enemy_info(players_for_simulation, player, ah_map)
    to_ah = None
    # Choose the enemy
    for j, min_k in enumerate(enemy_mins):
        if min_k == float('inf'):
            continue
        min_ah = ah_map.player_ahs[players_for_simulation[j]][min_k]
        if min_ah.get_population() < CRITICAL_POPULATION:
            to_ah = min_ah
    if to_ah is None:
        min_sum_index = np.argmin(enemy_sums)
        if enemy_sums[min_sum_index] == float('inf'):
            return None
        #min_sum_index, _ = min(enumerate(enemy_sums), key=operator.itemgetter(1))
        enemy_ahs = ah_map.player_ahs[players_for_simulation[min_sum_index]]
        to_ah = enemy_ahs[enemy_mins[min_sum_index]]
    return to_ah

def simulate_players(players_for_simulation, ah_map : Map, simulate_player = False):
    '''Simulates bots (+player) movements'''
    for player in players_for_simulation:
        # If main player simulation is not chosen then skip him
        if not simulate_player:
            if player == ah_map.current_player:
                continue
        # Is player even alive?
        players_ahs = ah_map.player_ahs[player]
        if len(players_ahs) == 0:
            continue
        # Random chance he wont play
        if randint(0,99) < 100 - CHANCE_OF_PLAYING:
            continue

        # Choose source
        from_ah, _, min_i = __choose_source(players_ahs)

        # choose target
        to_ah = None
        to_ah = __choose_target(players_ahs, players_for_simulation, from_ah, player, min_i, ah_map)

        # send ants to target
        if to_ah is None:
            continue
        else:
            ah_map.send_ants(from_ah, to_ah)
