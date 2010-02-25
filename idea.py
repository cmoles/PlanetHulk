# Characters - Hulk, Spider-man, Captain America, Dr. Doom
    # Animations - Walk, Run, Fly, Fight
    # Health
import os 
import pygame
from pygame.locals import *
from random import randint
from hulk import hulk_data

RESOLUTION = (640, 480)

pygame.init()
screen       = pygame.display.set_mode(RESOLUTION)
background   = pygame.Surface(RESOLUTION)
default_font = pygame.font.get_default_font()
font         = pygame.font.SysFont(default_font, 20, False)    

background.fill((255,175,175))

screen.blit(background, (0, 0))

class Animation():
    def __init__(self,images,offsets,file_image,fps=10):
        self._images        = load_sliced_sprites(images,file_image)
        self._offsets       = offsets
        self._delay         = 1000 / fps
        self.start(0)
    def __str__(self):
        return "[%s - %s]" % (self.image,self.offpt)
    def start(self,t):
        self._last_update   = t
        self._frame         = 0
        self.image          = self._images[self._frame]
        self.offpt          = self._offsets[self._frame]
    def update(self,t):
        if t - self._last_update >= self._delay:
            self._frame += 1
            if self._frame >= len(self._images):
                self._frame = 0
            self.image = self._images[self._frame]
            self.offpt = self._offsets[self._frame]
            self._last_update = t

class Fighter():
    def __init__(self,health,location):
        self.health     = health
        self.location   = location
        self._animation = ''
        self.animations = {}
    def __str__(self):
        """
        anims = "\n\t".join("%s - %s" % (key, anim)
                    for key, anim in self.animations.items())
        """
        if self.animations:
            frame = "%s (%s)" % (self.state()._frame,len(self.state()._images))
        else:
            frame = ""
        return "%s - %s : %s - %s" % \
            (self.health,self.location,self._animation,frame)
    def state(self):
        return self.animations[self._animation]
    def update(self,t):
        self.state().update(t)
    def render(self,screen):
        screen.blit(self.state().image,self.location)

class Hulk(Fighter):
    def __init__(self,location):
        Fighter.__init__(self,999,location) 
        self._animation = 'walk'
        for key, val in hulk_data.items():
            self.animations[key] = Animation(val['rects'],
                                             val['offpt'],
                                             val['image'])
    def update(self,t):
        Fighter.update(self,t)

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
    hero = Fighter(100,[10,20])
    hulk = Hulk([50,20])
    print "hero - %s" % hero
    print "hulk - %s" % hulk
    for t in xrange(0,1000,100):
        t += 100
        screen.blit(background, (0, 0))
        hulk.update(t)
        hulk.render(screen)
        print "hulk - %s" % hulk
        pygame.display.update()

if __name__ == "__main__": run()
