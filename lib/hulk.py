from pygame.constants import *
from objects import Animation, Fighter, Logo

HULK_STATE_DATA = {
    'walk': {
        'force':(.25,0),
        'nexts':{
            K_a     :{
                'state':'walk',
                'direc':-1
                'picku':True
                'backs':''},
            K_a     :{
                'state':'walk',
                'direc':-1},
            K_a     :{
                'state':'walk',
                'direc':-1},
            K_a     :{
                'state':'walk',
                'direc':-1},
    },
    'stay': {
        'force':(0,0),
        'nexts':{
            K_a     :('walk',-1),
            K_d     :('walk', 1),
            K_SPACE :('punk', 0),},
    },
    'punk': {
        'force':(0,0),
        'nexts':{
            K_a     :('walk',-1),
            K_d     :('walk', 1),
            K_SPACE :('pun2', 0),},
        'after':'stay',
    },
}

HULK_STATE_DATA_BAK = {
    'walk': {
        'force':(.25,0),
        'click':{
            K_a     :('walk',-1),
            K_d     :('walk', 1),
            K_SPACE :('punk', 0),},
    },
    'stay': {
        'force':(0,0),
        'click':{
            K_a     :('walk',-1),
            K_d     :('walk', 1),
            K_SPACE :('punk', 0),},
    },
    'punk': {
        'force':(0,0),
        'click':{
            K_a     :('walk',-1),
            K_d     :('walk', 1),
            K_SPACE :('pun2', 0),},
        'after':'stay',
    },
}


HULK_IMAGE_DATA = {
    'walk': {
        'rects':[
            (  8, 156, 30, 66, +4, -1),
            ( 51, 158, 28, 68, +4, -4),
            ( 94, 158, 46, 66, -4, -2),
            (150, 157, 42, 65, -3, -1),
            (202, 158, 27, 66, +4, -2),
            (243, 157, 31, 67, +3, -3),
            (285, 160, 47, 65, -5, -1),
            (344, 159, 46, 64, -5, -1),],
        'slide':-10,
        'image':'theincrediblehulkwu6.png'
    },
    'dash': {
        'rects':[
            (  3, 243, 51, 45, +6, 17),
            ( 56, 242, 59, 48, -2, 14),
            (123, 242, 64, 50, -7, 12),
            (197, 242, 57, 48, +1, 14),
            (270, 246, 52, 45, +7, 17),
            (328, 245, 57, 47, -0, 15),
            (395, 245, 66, 45, -6, 17),
            (469, 239, 55, 53, +3,  9),],
        'slide':0,
        'image':'theincrediblehulkwu6.png'
    },
    'punk': {
        'rects':[
            (  5, 394, 51, 62, -6, 2),
            ( 63, 395, 47, 62, -2, 2),
            (117, 394, 68, 63,  2, 1),
            (191, 395, 47, 62,  3, 2),
            (250, 394, 69, 63,  3, 1),],
        'slide':3,
        'image':'theincrediblehulkwu6.png'
    },
    'stay': {
        'rects':[
            (184,  83, 39, 64, +1, 0),
            (230,  83, 40, 64,  0, 0),
            (275,  83, 40, 64,  0, 0),
            (319,  83, 41, 64, -1, 0),],
        'slide':0,
        'image':'theincrediblehulkwu6.png'
    },
}

class Hulk(Fighter):
    def __init__(self,location):
        Fighter.__init__(self,999,location,) 
        self._animation = 'stay'
        for key, val in HULK_IMAGE_DATA.items():
            self.animations[key] = Animation(**val)
    def update(self,t):
        Fighter.update(self,t)
        """
        if self.anime is 'jump':
            if self.state.done:
                self.change('stay',t)
                self.force((0,0))
        """
        if self.anime is 'punk':
            if self.state.done:
                self.change('stay',t)
                self.force((0,0))
    def finish(self,key,t):
        if key in [K_a,K_d,K_w,K_s]:
            self.change('stay',t)
            self.force((0,0))
        """
        if key is K_SPACE:
            self.change('stay',t)
            self.force((0,0))
        """
    def control(self,key,t):
        if key is K_s:
            self.turn(-1)
            self.change('dash',t)
            self.force((-1.75,0))
        if key is K_w:
            self.turn(1) 
            self.change('dash',t)
            self.force((1.75,0))
        if key is K_a:
            self.turn(-1) 
            self.change('walk',t)
            self.force((-.25,0))
        if key is K_d:
            self.turn(1)
            self.change('walk',t)
            self.force((.25,0))
        if key is K_SPACE:
            if self._animation is not 'punk':
                self.change('punk',t)
                self.force((0,0))

class HulkLogo(Logo):
    def __init__(self, location):
        logo_args = {
            'rects' : ([0, 0, 241, 94],),
            'image' : 'HulkLogo.gif',}
        Logo.__init__(self,location=location,**logo_args)

    
