import pygame, random, time, os
from pygame.constants import *
from hulk import Hulk

RESOLUTION = (640, 480)

class Game():
    def __init__(self,):
        pygame.init()
        self.screen         = pygame.display.set_mode(RESOLUTION)
        self.background     = pygame.Surface(RESOLUTION)
        self.default_font   = pygame.font.get_default_font()
        self.font           = pygame.font.SysFont(self.default_font, 20, False)
        self.running        = True
        
        self.background.fill((255,175,175))
        self.screen.blit(self.background, (0, 0))

        self.hulk           = Hulk([50,220])
        #self.hulk.turn()
    def loop(self,):
        user_keys = [K_a,K_w,K_s,K_d,K_SPACE]
        while self.running:
            for event in pygame.event.get():
                if event.type is QUIT               \
                        or event.type is KEYDOWN    \
                        and event.key in [K_q, K_ESCAPE]:
                    pygame.quit()
                    return
                if event.type is KEYDOWN:
                    if event.key in [K_f]:
                        pygame.display.toggle_fullscreen()
                    if event.key in user_keys:
                        self.hulk.control(event.key,pygame.time.get_ticks())
                if event.type is KEYUP:
                    if event.key in user_keys:
                        self.hulk.finish(event.key,pygame.time.get_ticks())
            self.screen.blit(self.background, (0, 0))
            self.hulk.update(pygame.time.get_ticks())
            self.hulk.render(self.screen)
            pygame.display.update()
