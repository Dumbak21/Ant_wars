'''GUI tests'''
import pygame
import pytest
import main
import model.gameState as gameState
from GUI.gui_manager import *
from GUI.button_manager import *
import GUI.gui_manager as gui_modul
from flexmock import flexmock

@pytest.mark.gui
@pytest.mark.timeout(10)
def test_pygame_window_created_and_destroyed():

    # create
    pygame.quit()
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

@pytest.mark.gui
@pytest.mark.run(after='test_pygame_window_created_and_destroyed')
class TestGUI:
    win = None

    def setup_method(self, method):
        '''
        Initialize window and start main event loop
        '''
        self.win = main.init_win()
        #main.main_loop(self.win)


    def teardown_method(self, method):
        '''
        close window and end pygame
        '''
        main.destr_game()


    def test_button(self):
        '''Button'''
        btn = Button(0, 0, 'Btn', 1, (255,255,255), None, font=pygame.font.SysFont('comicsans', 40))
        assert btn is not None
        img = pygame.Surface((1,1))
        btn = Button(0, 0, 'Btn', 1, img=img)
        assert btn is not None

        with pytest.raises(ValueError):
            Button(0, 0, 'Btn', 1, None, None, font=pygame.font.SysFont('comicsans', 40))
        with pytest.raises(ValueError):
            Button(0, 0, 'Btn', 1, (255,255,255), None)
        with pytest.raises(ValueError):
            Button(0, 0, 'Btn', 1, None, None)

    def test_button_clr(self):
        '''Text button, placement'''
        btn = ButtonClr(0, 0, 'Btn', 1, (255,255,255), None, font=pygame.font.SysFont('comicsans', 40))
        assert btn is not None

        rect = btn.draw_btn(self.win, 1)
        assert rect is not None

        with pytest.raises(ValueError):
            ButtonClr(0, 0, 'Btn', 1, None, None, font=pygame.font.SysFont('comicsans', 40))
        with pytest.raises(ValueError):
            ButtonClr(0, 0, 'Btn', 1, (255,255,255), None)
        with pytest.raises(ValueError):
            ButtonClr(0, 0, 'Btn', 1, None, None)


    def test_handle_loose(self):
        flexmock(gui_modul).should_call('draw_loose').once()
        main.draw_loose = gui_modul.draw_loose
        main.handle_loose(self.win)

    def test_handle_win(self):
        flexmock(gui_modul).should_call('draw_win').once()
        main.draw_win = gui_modul.draw_win
        main.handle_win(self.win)

    def test_handle_next(self):
        flexmock(gui_modul).should_call('draw_next_round').once()
        main.draw_next_round = gui_modul.draw_next_round
        main.handle_next_round(self.win)



    @pytest.mark.run(after='test_button_clr')
    def test_button_click(self):
        btn = ButtonClr(0, 0, 'Btn', 1, (255,255,255), None, font=pygame.font.SysFont('comicsans', 40))
        x_loc, y_loc = 1,1
        pygame.mouse.set_pos((x_loc, y_loc))
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=0))
        state, _ = draw_button(self.win, btn, x_loc, y_loc, gameState.GameState.PLAY)
        assert state == gameState.GameState.PLAY


    # @pytest.mark.parametrize('draw_method', [draw_loose, draw_win, draw_next_round])
    # def test_draw(self, draw_method):
    #     self.win.should_receive('blit').at_least().once()
    #     draw_method(self.win)
