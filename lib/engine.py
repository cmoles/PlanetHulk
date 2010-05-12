import pygame

class Keyboard(object):
    """Store Key information for each character
    as a tuple by the following order:

    0 State - Up / Down (False / True)
    1 Ticks - Lenght since last action"""
    _keys = {}
    _char = {}
    @property
    def keys():
        return self._keys
    def key_change(self,key,press,ticks):
        self._keys[key] = {'press':press,'time':ticks}
    """
    def update(event,ticks):
        self._keys[event.key] = {'type':event.type,'time':ticks}
    """
    def key_down(self,key,ticks):
        self._keys[key] = {'press':True,'time':ticks}
    def key_up(self,key,ticks):
        self._keys[key] = {'press':False,'time':ticks}
    """
    def keys_down(self,keys,ticks):
        for key in keys:
            self._keys[key] = (True,ticks)
    def keys_up(self,keys,ticks):
        for key in keys:
            self._keys[key] = (False,ticks)
    """
    def attach(self,user,user_keys):
        """For lack of a better name, the user is a character
        controlled by the keyboard: User must be first 
        attached to keyboard with keys own set of keys."""
        self._char[user] = user_keys
    def char_keys(self,user,):
        return ((key,time) 
            for key,time in self._keys 
                if key in self._char[user])

