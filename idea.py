import os 
import pygame
from pygame.locals import *
from random import randint
execfile('hulk.py')

RESOLUTION = (640, 480)

pygame.init()
screen       = pygame.display.set_mode(RESOLUTION)
background   = pygame.Surface(RESOLUTION)
default_font = pygame.font.get_default_font()
font         = pygame.font.SysFont(default_font, 20, False)    

background.fill((255,175,175))

screen.blit(background, (0, 0))

class Animation():
    def __init__(self,images,offsets,slide,file_image,flip=False,fps=10):
        self._imagesR       = load_sliced_sprites(images,file_image,flip)
        self._imagesL       = load_sliced_sprites(images,file_image,not flip)
        self.flip           = flip
        self._offsetsR      = offsets
        self._offsetsL      = flip_offsets(images,offsets,slide)
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
        if direction == None:
            if self.direction == 1:
                self.direction = -1
                self.state().flip = True
            else:
                self.direction = 1
                self.state().flip = False
        else:
            self.direction = direction
            self.state().flip = direction == -1 and True
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

class Hulk(Fighter):
    def __init__(self,location):
        Fighter.__init__(self,999,location,) 
        self._animation = 'stay'
        for key, val in hulk_data.items():
            self.animations[key] = Animation(val['rects'],
                                             val['offpt'],
                                             val['slide'],
                                             val['image'])
    def update(self,t):
        Fighter.update(self,t)
        if self.anime() == 'jump':
            if self.state().done:
                self.change('stay',t)
                self.force((0,0))
        """
        if self.anime() == 'punk':
            if self.state().done:
                self.change('stay',t)
                self.force((0,0))
        """
    def finish(self,key,t):
        if key == K_a:
            self.change('stay',t)
            self.force((0,0))
        if key == K_d:
            self.turn(1)
            self.change('stay',t)
            self.force((0,0))
        if key == K_SPACE:
            self.change('stay',t)
            self.force((0,0))
    def control(self,key,t):
        if key == K_s:
            if not self.anime() == 'stay':
                self.change('stay',t)
                self.force((0,0))
        if key == K_a:
            self.turn(-1) 
            self.change('walk',t)
            self.force((-.25,0))
        if key == K_d:
            self.turn(1)
            self.change('walk',t)
            self.force((.25,0))
        if key == K_SPACE:
            self.change('punk',t)
            self.force((0,0))

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
            simg = pygame.transform.flip(sheet.subsurface(srect), 1, 0).convert()
        else:
            simg = sheet.subsurface(srect).convert()
        simg.set_colorkey(simg.get_at((0, 0)), RLEACCEL)
        images.append(simg)
    return images

def run():
    hulk = Hulk([50,220])
    user_keys = [K_a,K_w,K_s,K_d,K_SPACE]
    hulk.turn()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT               \
                    or event.type == KEYDOWN    \
                    and event.key in [K_q, K_ESCAPE]:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key in [K_f]:
                    pygame.display.toggle_fullscreen()
                if event.key in user_keys:
                    hulk.control(event.key,pygame.time.get_ticks())
            if event.type == KEYUP:
                if event.key in user_keys:
                    hulk.finish(event.key,pygame.time.get_ticks())
        screen.blit(background, (0, 0))
        hulk.update(pygame.time.get_ticks())
        hulk.render(screen)
        pygame.display.update()

if __name__ == "__main__": run()
