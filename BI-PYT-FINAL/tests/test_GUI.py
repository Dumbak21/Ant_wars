import pygame
import pytest

import main

@pytest.mark.gui
@pytest.mark.timeout(10)
def test_pygame_window_created_and_destroyed():

    # create
    win = main.init_win()
    assert win is not None
    assert pygame.get_init()
    assert pygame.display.get_init()

    events = pygame.event.get()
    window_exists = False
    for ev in events:
        if ev.type == pygame.WINDOWSHOWN:
            window_exists = True
    assert window_exists


    # destroy
    assert pygame.event.post(pygame.event.Event(pygame.QUIT))
    main.main_loop(win)

    assert pygame.get_init()
    assert not pygame.display.get_init()
    # events = pygame.event.get()
    # window_exists = True
    # for ev in events:
    #     print(pygame.event.event_name(ev.type))
    #     if ev.type == pygame.WINDOWCLOSE:
    #         window_exists = False
    #     #pygame.event.post(ev)
    # assert not window_exists

    main.destr_game()

    assert not pygame.get_init()

@pytest.mark.run(after='test_pygame_window_created_and_destroyed')
class TestGUI:
    win = None

    def setup_method(self, method):
        '''
        Initialize window and start main event loop
        '''
        self.win = main.init_win()
        main.main_loop(self.win)


    def teardown_method(self, method):
        '''
        close window and end pygame
        '''
        main.destr_game()



    # def test_pygame_window_created_and_closed(self):
    #     assert True
