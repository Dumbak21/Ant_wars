'''
Manages buttons, its vizualization and position
'''

import pygame

pygame.font.init()

MENU_BTN_FONT = pygame.font.SysFont('comicsans', 40)
EXIT_FONT = pygame.font.SysFont('comicsans', 20)

WHITE = (255,255,255)

class Button:
    '''Button - parent class for all buttons - prepares for visualization'''
    def __init__(self, x_loc, y_loc, text = '', scale = 1, text_color = None,\
            border_color = None, border_width=2, font = None, img = None) -> None:
        self.focused = False
        #self.x = x
        #self.y = y
        self.color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.__img = img
        self.is_img = False

        if self.color is None and self.__img is None:
            raise Exception("wrong button color or img")

        if img is not None:
            self.__img = pygame.transform.scale(img, (int(img.get_width() * scale),\
                                                    int(img.get_height() * scale)))
            self.is_img = True
            self.rect = self.__img.get_rect()
            self.rect.topleft = (x_loc,y_loc)
        if self.color is not None:
            if font is None:
                raise Exception("Missing font")

            if self.border_color is None:
                self.border_color = self.color

            self.text = font.render(text, 1, self.color)
            self.width = self.text.get_width()
            self.height = self.text.get_height()
            self.rect = pygame.Rect(x_loc,y_loc, self.width, self.height)

    def set_coords(self, x_loc, y_loc):
        '''Set coords of top left point of button'''
        self.rect.x = x_loc
        self.rect.y = y_loc


# class ButtonImg(Button):
#     def __init__(self, x, y, scale=1, border_color=None, img=None) -> None:
#          super().__init__(x, y, scale, border_color, img)

#     def draw_btn(self, WIN):
#         pass

class ButtonClr(Button):
    '''Button with text'''
    def __init__(self, x, y, text='', scale=1, text_color=None,\
                border_color=None, border_width=2, font=None) -> None:
        super().__init__(x, y, text, scale, text_color, border_color, border_width, font)

    def draw_btn(self, WIN, scale = 1):
        '''Draws this button on WIN screen in scale'''
        scaled_rect = pygame.Rect(self.rect)
        old_w = scaled_rect.w
        old_h = scaled_rect.h
        scaled_rect.w *= scale
        scaled_rect.h *= scale
        scaled_rect.x -= (scaled_rect.w - old_w) //2
        scaled_rect.y -= (scaled_rect.h - old_h) //2
        pygame.draw.rect(WIN ,rect=scaled_rect, color=self.border_color,\
                     width=self.border_width, border_radius=2)
        WIN.blit(self.text, (self.rect.x, self.rect.y))
        return scaled_rect


play_game_btn = ButtonClr(0, 0, 'PLAY', text_color=WHITE, font=MENU_BTN_FONT)
exit_btn = ButtonClr(0, 0, 'EXIT', text_color=WHITE, font=MENU_BTN_FONT)

exit_game_btn = ButtonClr(0, 0, 'EXIT', text_color=WHITE, font=EXIT_FONT)
