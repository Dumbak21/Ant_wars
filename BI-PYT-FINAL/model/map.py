from model.anthill import Anthill
from model.player import Player
from model.ant import Ant

ANT_FORMATION_SIZE = 5

ANT_STEP_SIZE = 10

class Map:
    '''Map - interactions with map elements.'''
    def __init__(self, anthills = None, ah_coords = None, player_ahs = None, players = None,\
                ant_coords = None, player_colors = None, current_player : Player = None,\
                selected_ah = None, play_state = None):
        if anthills is None:
            self.anthills = []
        else:
            self.anthills = anthills

        if ah_coords is None:
            self.ah_coords = {}
        else:
            self.ah_coords = ah_coords

        if player_ahs is None:
            self.player_ahs = {}
        else:
            self.player_ahs = player_ahs

        if players is None:
            self.players = []
        else:
            self.players = players

        if ant_coords is None:
            self.ant_coords = {}
        else:
            self.ant_coords = ant_coords

        if player_colors is None:
            self.player_colors = {}
        else:
            self.player_colors = player_colors

        if current_player is None:
            self.current_player = None
        else:
            self.current_player = current_player

        if selected_ah is None:
            self.selected_ah = None
        else:
            self.selected_ah = selected_ah

        if play_state is None:
            self.play_state = None
        else:
            self.play_state = play_state


    def place_anthill(self, ah : Anthill, x_loc, y_loc):
        '''Places anthill on location'''
        self.ah_coords[ah] = (x_loc,y_loc)
        self.anthills.append(ah)
        ah.x_loc = x_loc
        ah.y_loc = y_loc
        if ah.owner is not None:
            if ah.owner in self.player_ahs:
                self.player_ahs[ah.owner].append(ah)
            else:
                self.player_ahs[ah.owner] = [ah]

    def ah_change_owner(self, ah : Anthill, new_owner : Player):
        '''Change owner of anthill'''
        # Remove from old player
        if ah.owner in self.player_ahs:
            if ah in self.player_ahs[ah.owner]:
                self.player_ahs[ah.owner].remove(ah)
        # Add to new player
        if new_owner in self.player_ahs:
            self.player_ahs[new_owner].append(ah)
        else:
            self.player_ahs[new_owner] = [ah]
        ah.change_owner(new_owner)

    def inc_anthills(self):
        '''Inc all anthills on map'''
        for ah in self.anthills:
            ah.inc()

    def send_ants(self, from_ah : Anthill, to_ah : Anthill, count = ANT_FORMATION_SIZE):
        '''Schedule ants to send from one anthill to another'''
        from_ah.send_ants(count, to_ah)

    def assign_empty_ahs(self, new_owner : Player):
        '''Assign anthills without owner to someone'''
        for ah in self.anthills:
            if ah.owner is None:
                if new_owner in self.player_ahs:
                    self.player_ahs[new_owner].append(ah)
                else:
                    self.player_ahs[new_owner] = [ah]
                ah.change_owner(new_owner)

    def get_ah_cnt(self):
        '''Return anthill count on map'''
        return len(self.anthills)

    def __get_ants_to_spawn(self):
        ants_to_spawn = []
        for ah in self.anthills:
            attacking_enemies = ah.update()
            for to_ah in attacking_enemies:
                ants_to_spawn.append((ah, to_ah))
        return ants_to_spawn

    def __spawn_ants_at_home(self, ants_to_spawn):
        for from_ah, to_ah in ants_to_spawn:
            ant = Ant(from_ah, to_ah, from_ah.owner)
            coords = self.ah_coords[from_ah]
            x_loc, y_loc = coords
            self.ant_coords[ant] = x_loc, y_loc

    def __update_ants_loc(self, determine_pos_fnc, ant_step_size):
        new_ant_coords = {}
        for ant, _ in self.ant_coords.items():
            new_loc = determine_pos_fnc(ant, self, ant_step_size)
            new_ant_coords[ant] = new_loc
            ant.x_loc, ant.y_loc = new_loc
        self.ant_coords = new_ant_coords


    def update(self):
        '''Update map (spawn ants, move ants)'''
        # Get ants ready to be spawn
        ants_to_spawn = self.__get_ants_to_spawn()
        # Move all ants in direction of target anthill
        self.__update_ants_loc(get_new_ant_loc, ANT_STEP_SIZE)
        # Spawn ants at home anthill
        self.__spawn_ants_at_home(ants_to_spawn)


# Any algorithm for making path (potencialy could be bfs, but excessive here)
def get_new_ant_loc(ant : Ant, map: Map, step_size):
    '''Algorithm for making path (potencialy could be bfs, but excessive here)'''
    coords = map.ant_coords[ant]
    curr_x, curr_y = coords
    curr_x += ant.width//2
    curr_y += ant.height//2

    to_ah_loc = map.ah_coords[ant.to_ah]
    to_x, to_y = to_ah_loc
    to_x += ant.to_ah.width//2
    to_y += ant.to_ah.height//2

    if abs(curr_x - to_x) > abs(curr_y - to_y):
        # x
        if curr_x > to_x:
            return (curr_x - step_size - ant.width//2 , curr_y - ant.height//2)
        else:
            return (curr_x + step_size - ant.width//2, curr_y - ant.height//2)
    else:
        if curr_y > to_y:
            return (curr_x - ant.width//2, curr_y - step_size - ant.height//2)
        else:
            return (curr_x - ant.width//2, curr_y + step_size - ant.height//2)
