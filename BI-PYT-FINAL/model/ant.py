from model.map_elem import MapElem
from model.anthill import Anthill
from model.player import Player

class Ant(MapElem):
    '''Ant - has source and target, and its owner'''
    def __init__(self, from_ah : Anthill, to_ah : Anthill, owner : Player,\
                x_loc=None, y_loc=None, width=None, height=None):
        super().__init__(x_loc, y_loc, width, height)
        self.from_ah = from_ah
        self.to_ah = to_ah
        self.owner = owner
