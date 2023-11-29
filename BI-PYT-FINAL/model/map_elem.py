from abc import ABC

class MapElem(ABC):
    '''Parent class for all map elements'''
    def __init__(self, x_loc, y_loc, width, height) -> None:
        self.x_loc = x_loc
        self.y_loc = y_loc

        self.width = width
        self.height = height
