########################################################################
## Project: Planet Hulk
## Author: Chris Moles
##
## This project is for educational purposes only. I love the Hulk and 
## all of Marvel's characters, and this game is to have fun with them
## while learning the fun possibilities of PyGame.
##
## Please don't sue.
########################################################################

import os 
import pygame
from pygame.locals import *
from random import randint

RESOLUTION = (640, 480)

hulk_data = {
    'walk': {
        'rects':[
            (  8, 156, 30, 66),
            ( 51, 158, 28, 68),
            ( 94, 158, 46, 66),
            (150, 157, 42, 65),
            (202, 158, 27, 66),
            (243, 157, 31, 67),
            (285, 160, 47, 65),
            (344, 159, 46, 64),],
        'offpt':[
            (  +4,  -1),
            (  +4,  -4),
            (  -4,  -2),
            (  -3,  -1),
            (  +4,  -2),
            (  +3,  -3),
            (  -5,  -1),
            (  -5,  -1),],
    },
   'dash': {
       'rects':[
            (  3, 243, 51, 45),
            ( 56, 242, 59, 48),
            (123, 242, 64, 50),
            (197, 242, 57, 48),
            (270, 246, 52, 45),
            (328, 245, 57, 47),
            (395, 245, 66, 45),
            (469, 239, 55, 53),
       ],
       'offpt':[
            ( +6,   17),
            ( -2,   14),
            ( -7,   12),
            ( +1,   14),
            ( +7,   17),
            ( -0,   15),
            ( -6,   17),
            ( +3,   9),]
    },
   'punk': {
       'rects':[
            (  5, 394, 51, 62),
            ( 63, 395, 47, 62),
            (117, 394, 68, 63),
            (191, 395, 47, 62),
            (250, 394, 69, 63),
       ],
       'offpt':[
            ( -6,   2),
            ( -2,   2),
            (  2,   1),
            (  3,   2),
            (  3,   1),]
    },
   'stay': {
       'rects':[
            (184,  83, 39, 64),
            (230,  83, 40, 64),
            (275,  83, 40, 64),
            (319,  83, 41, 64),
       ],
       'offpt':[
            ( +1,   0),
            (  0,   0),
            (  0,   0),
            ( -1,   0),
       ],
   }
}

pygame.init()
screen       = pygame.display.set_mode(RESOLUTION)
background   = pygame.Surface(RESOLUTION)
default_font = pygame.font.get_default_font()
font         = pygame.font.SysFont(default_font, 20, False)    

background.fill((255,175,175))

screen.blit(background, (0, 0))

class HulkError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class HulkSprite(pygame.sprite.Sprite):
    def __init__(self, hulk_data_images, hulk_data_offset, state, fps = 10, location = (30, 300)):
        pygame.sprite.Sprite.__init__(self)
        self._images            = hulk_data_images
        self._offsets           = hulk_data_offset
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start             = pygame.time.get_ticks()
        self._delay             = 1000 / fps
        self._last_update       = 0
        self._frame             = 0
        self.state              = state
        self.image              = self._images[self.state][self._frame]
        self.offpt              = self._offsets[self.state][self._frame]
        # Defining a default location on screen for our sprite
        w, h                    = RESOLUTION
        self.location           = location
        self.position           = self.shift()
    def shift(self):
        x, y = self.location
        j, k = self.offpt
        return x + j, y + k
    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.
        if t - self._last_update > self._delay:
            self._frame += 1
            # Animation Finished, choosing a new location
            if self._frame >= len(self._images[self.state]):
                self._frame = 0
            self.image = self._images[self.state][self._frame]
            self.offpt = self._offsets[self.state][self._frame]
            if self.state == 'punk':
                self.move((0,0))
            elif self.state == 'walk':
                self.move((6,0))
            elif self.state == 'dash':
                self.move((25,0))
            elif self.state == 'stay':
                self.move((0,0))
            self._last_update = t
    def move(self, distance):
        x, y = self.location
        j, k = self.offpt
        x += distance[0]
        y += distance[1]
        if x > RESOLUTION[0]:
            x = j - self.image.get_size()[0]
        self.location = x, y
        self.position = self.shift()
    def toggle_state(self):
        if self.state == 'stay':
            self.state = 'punk'
        elif self.state == 'punk':
            self.state = 'walk'
        elif self.state == 'walk':
            self.state = 'dash'
        elif self.state == 'dash':
            self.state = 'stay'
    def render(self, screen):
        self.update(pygame.time.get_ticks())
        screen.blit(self.image, self.position)

class Logo(pygame.sprite.Sprite):
    def __init__(self, image, location):
        self.image = image
        self.location = location
    def render(self, screen):
        screen.blit(self.image, self.location)

def load_sliced_sprites(sprite_images, filename):
    images = []
    sheet  = pygame.image.load(os.path.join('data', filename)).convert_alpha()
    for srect in sprite_images:
        #simg = pygame.transform.flip(sheet.subsurface(srect), 1, 0).convert()
        simg = sheet.subsurface(srect).convert()
        simg.set_colorkey(simg.get_at((0, 0)), RLEACCEL)
        images.append(simg)
    return images


def run():    
    hulk_walk_images      = load_sliced_sprites(hulk_data['walk']['rects'], 'theincrediblehulkwu6.png')
    hulk_dash_images      = load_sliced_sprites(hulk_data['dash']['rects'], 'theincrediblehulkwu6.png')
    hulk_stay_images      = load_sliced_sprites(hulk_data['stay']['rects'], 'theincrediblehulkwu6.png')
    hulk_punk_images      = load_sliced_sprites(hulk_data['punk']['rects'], 'theincrediblehulkwu6.png')
    hulk_walk_offset      = hulk_data['walk']['offpt']
    hulk_dash_offset      = hulk_data['dash']['offpt']
    hulk_stay_offset      = hulk_data['stay']['offpt']
    hulk_punk_offset      = hulk_data['punk']['offpt']
    hulk_images           = {'walk': hulk_walk_images, 'dash': hulk_dash_images, 'stay': hulk_stay_images, 'punk': hulk_punk_images}
    hulk_offset           = {'walk': hulk_walk_offset, 'dash': hulk_dash_offset, 'stay': hulk_stay_offset, 'punk': hulk_punk_offset}

    clock                 = pygame.time.Clock()
    
    sprites               = []
    hulk                  = HulkSprite(hulk_images, hulk_offset, 'stay', 15, (300, 300))
    #hulk                  = HulkSprite(hulk_images, hulk_offset, 'punk', 1, (200, 300))
    logo                  = Logo(load_sliced_sprites(([0, 0, 241, 94],),'HulkLogo.gif')[0], (200, 50))
    sprites.append(hulk)
    sprites.append(logo)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]:
                return
            if event.type == KEYDOWN:
                if event.key in [K_f]:
                    pygame.display.toggle_fullscreen()
                if event.key in [K_SPACE]:
                    hulk.toggle_state()
        screen.blit(background, (0, 0))
        time_passed = clock.tick(30)
        for sprite in sprites:
            sprite.render(screen)
        pygame.display.update()


if __name__ == "__main__": run()
