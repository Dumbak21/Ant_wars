class Player:
    '''Player - bot or actuall player, holds nickname and number of its anthills in game'''
    def __init__(self, _name : str, ah_count : int = 0) -> None:
        if _name is None or _name == "" or ah_count < 0:
            raise ValueError
        if not isinstance(_name, str):
            raise TypeError
        self.name = _name
        self.number_of_ahs = ah_count

    def lost_ah(self):
        '''Dec number of anthills'''
        if self.number_of_ahs > 0:
            self.number_of_ahs -= 1

    def gained_ah(self):
        '''Inc number of anthills'''
        self.number_of_ahs += 1

    def get_ah_cnt(self):
        '''Returns number of anthills'''
        return self.number_of_ahs

    def reset(self):
        '''Resets number of anthills'''
        self.number_of_ahs = 0

    def get_name(self) -> str:
        '''Return name'''
        return self.name
