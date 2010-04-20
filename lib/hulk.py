from pygame.constants import *
from objects import Animation, Fighter

HULK_DATA = {
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
       'slide':-10,
       'image':'theincrediblehulkwu6.png'
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
            ( +3,   9),],
       'slide':0,
       'image':'theincrediblehulkwu6.png'
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
            (  3,   1),],
       'slide':3,
       'image':'theincrediblehulkwu6.png'
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
            ( -1,   0),],
       'slide':0,
       'image':'theincrediblehulkwu6.png'
   }
}

class Hulk(Fighter):
    def __init__(self,location):
        Fighter.__init__(self,999,location,) 
        self._animation = 'stay'
        for key, val in HULK_DATA.items():
            self.animations[key] = Animation(val['rects'],
                                             val['offpt'],
                                             val['slide'],
                                             val['image'])
    def update(self,t):
        Fighter.update(self,t)
        if self.anime() is 'jump':
            if self.state().done:
                self.change('stay',t)
                self.force((0,0))
        if self.anime() is 'punk':
            if self.state().done:
                self.change('stay',t)
                self.force((0,0))
    def finish(self,key,t):
        if key is K_a:
            self.change('stay',t)
            self.force((0,0))
        if key is K_d:
            self.turn(1)
            self.change('stay',t)
            self.force((0,0))
        """
        if key is K_SPACE:
            self.change('stay',t)
            self.force((0,0))
        """
    def control(self,key,t):
        if key is K_s:
            if not self.anime() is 'stay':
                self.change('stay',t)
                self.force((0,0))
        if key is K_a:
            self.turn(-1) 
            self.change('walk',t)
            self.force((-.25,0))
        if key is K_d:
            self.turn(1)
            self.change('walk',t)
            self.force((.25,0))
        if key is K_SPACE and self._animation is not 'punk':
            self.change('punk',t)
            self.force((0,0))

