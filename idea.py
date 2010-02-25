# Characters - Hulk, Spider-man, Captain America, Dr. Doom
    # Animations - Walk, Run, Fly, Fight
    # Health
    
class Animation():
    def __init__(self,images,offsets,fps=10):
        self._images        = images
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
        if t - self._last_update > self._delay:
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
        anims = " ".join("%s - %s" % (key, anim) \
                    for key, anim in self.animations.items())
        return "%s - %s : %s" % (self.health,self.location,anims)
    def update(self,t):
        pass

class Hulk(Fighter):
    def __init__(self,location):
        Fighter.__init__(self,999,location) 
        self._animation = 'walk'
        self.animations = {'walk':Animation([1,2,3],[1,2,3])}
    def update(self,t):
        self.animations[self._animation].update(t)

def run():
    hero = Fighter(100,[10,20])
    hulk = Hulk([50,20])
    print "hero - %s" % hero
    print "hulk - %s" % hulk
    hulk.update(101)
    print "hulk - %s" % hulk

if __name__ == "__main__": run()
