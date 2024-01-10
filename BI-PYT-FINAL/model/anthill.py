from model.player import Player
from model.map_elem import MapElem

class Anthill(MapElem):
    '''Anthill - handles interaction with it'''
    def __init__(self, owner : Player, population = 0, available_ants = 0, queue_to_send = None,\
                clicked = False, x_loc=None, y_loc=None, width=None, height=None) -> None:
        super().__init__(x_loc, y_loc, width, height)

        if available_ants > population:
            raise ValueError("more available ants than is ah population")
        self.population = population
        self.available_ants = available_ants


        self.owner = owner
        # assign to owner
        if self.owner is not None:
            self.owner.gained_ah()

        # send queue copy
        if queue_to_send is None:
            self.queue_to_send = {}
        else:
            self.queue_to_send = queue_to_send

        self.clicked = clicked

    def get_population(self, only_available = False):
        '''Returns population/available population od anthill'''
        if only_available:
            return self.available_ants
        return self.population

    def get_queue_to_send(self):
        '''ants Queue'''
        return self.queue_to_send

    def change_owner(self, new_owner : Player):
        '''Changes owner of anthill'''
        if self.owner is not None:
            self.owner.lost_ah()
        if new_owner is not None:
            new_owner.gained_ah()
        self.owner = new_owner

    def inc(self):
        '''Inc of anthills population'''
        self.population += 1
        self.available_ants += 1

    def accept_ants(self, count):
        '''Add number of ants to anthill population'''
        if count < 0:
            raise ValueError("Use kill_ants for negative count")
        self.population += count
        self.available_ants += count

    def kill_ants(self, count):
        '''
        Substract number of ants from anthill population
        Returns True if killed ah
        '''
        if count < 0:
            raise ValueError("Use accept_ants for negative count")
        self.population -= count
        self.available_ants -= count

        if self.population < 0:
            #self.change_owner(by)
            self.population = abs(self.population)
            self.available_ants = self.population
            self.queue_to_send = {}
            return True
        return False

    def send_ants(self, count, to_ah : 'Anthill'):
        '''Send ants from this anthill to another'''
        if count < 0:
            raise ValueError
        if self.available_ants < count:
            count = self.available_ants
        if to_ah in self.queue_to_send:
            self.queue_to_send[to_ah] += count
        else:
            self.queue_to_send[to_ah] = count
        self.available_ants -= count
        return count

    def update(self):
        '''Update anthill to new round (send scheduled ants)'''
        attacking_enemies = []
        to_del = []
        for to, cnt in self.get_queue_to_send().items():
            if cnt > 0:
                attacking_enemies.append(to)
                self.queue_to_send[to] -= 1
                self.population -= 1
            if cnt == 0:
                to_del.append(to)
        for to in to_del:
            del self.get_queue_to_send()[to]
        return attacking_enemies
