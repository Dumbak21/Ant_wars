class Player:
    '''Player - bot or actuall player, holds nickname and number of its anthills in game'''
    def __init__(self, _name, ah_count = 0) -> None:
        self.name = _name
        self.number_of_ahs = ah_count

    def lost_ah(self):
        '''Dec number of anthills'''
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
