import os 
import pygame
from pygame.locals import *
from random import randint

class Animation():
    def __init__(self,images,slide,file_image,flip=False,fps=10):
        self._imagesR       = load_sliced_sprites(images,file_image,flip)
        self._imagesL       = load_sliced_sprites(images,file_image,not flip)
        self.flip           = flip
        self._offsetsR      = [a[4:] for a in images]
        self._offsetsL      = flip_offsets(images,self._offsetsR,slide)
        self._delay         = 1000 / fps
        self.start(0)
    def start(self,t):
        self._last_update   = t
        self._frame         = 0
        self.done           = False
        self.setimg()
    def setimg(self):
        if self.flip:
            self.image = self._imagesL[self._frame]
            self.offpt = self._offsetsL[self._frame]
        else:
            self.image = self._imagesR[self._frame]
            self.offpt = self._offsetsR[self._frame]
    def update(self,t):
        if t - self._last_update >= self._delay:
            self._frame += 1
            if self._frame >= len(self._imagesR):
                self._frame = 0
                self.done = True
                return
            self.setimg()
            self._last_update = t

class Fighter():
    def __init__(self,health,location,):
        self.health     = health
        self.location   = location
        self.position   = location
        self._animation = ''
        self.animations = {}
        self.direction  = 1
        self.velocity   = (0,0)
    def state(self):
        return self.animations[self._animation]
    def anime(self):
        return self._animation
    def shift(self):
        x,y = self.location
        j,k = self.state().offpt
        self.position = x+j,y+k
    def turn(self,direction=None):
        if direction is None:
            if self.direction is 1:
                self.direction = -1
                self.state().flip = True
            else:
                self.direction = 1
                self.state().flip = False
        else:
            self.direction = direction
            self.state().flip = direction is -1
    def change(self,state,t):
        self._animation = state
        self.turn(self.direction)
        self.state().start(t)
    def move(self,shift):
        x,y = self.location
        w,v = shift
        self.location = x+w,y+v
    def force(self,f):
        self.velocity = f
    def update(self,t):
        self.move(self.velocity)
        self.state().update(t)
    def render(self,screen):
        self.shift()
        screen.blit(self.state().image,self.position)

class Logo(pygame.sprite.Sprite):
    def __init__(self, location):
        self.image = load_sliced_sprites(([0, 0, 241, 94],),'HulkLogo.gif')[0]
        #self.location = (200, 50)
        self.location = location
    def render(self,screen):
        screen.blit(self.image, self.location)

def flip_offsets(images, offsets, slide):
    offsetmin   = min([offset[0] for offset in offsets])
    offsetmax   = max([offset[0] for offset in offsets])
    rights      = [offset[0] + image[2] 
                    for image, offset in zip(images, offsets)]
    rightmin    = min(rights)
    rightmax    = max(rights)
    """
    return [(rightmax - (rightmax - rightmin) - right - \
            (offsetmax - offsetmin), offset[1])
            for right, offset in zip(rights, offsets)]
    """
    return [(rightmin - right - offsetmax - slide, offset[1])
            for right, offset in zip(rights, offsets)]

def load_sliced_sprites(sprite_images, filename, flip=False):
    images = []
    sheet  = pygame.image.load(os.path.join('data', filename)).convert_alpha()
    for srect in sprite_images:
        if flip:
            simg = pygame.transform.flip(sheet.subsurface(srect[:4]), \
                                         1, 0).convert()
        else:
            simg = sheet.subsurface(srect[:4]).convert()
        simg.set_colorkey(simg.get_at((0, 0)), RLEACCEL)
        images.append(simg)
    return images

