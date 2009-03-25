'''
Copyright 2009 Paul Elms

This file is part of Froggix.

    Froggix is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Froggix is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Froggix.  If not, see <http://www.gnu.org/licenses/>.

'''
from pygame import *
from Sprite import Sprite

import random

class Moveable(Sprite):
    '''
    classdocs
    '''
    
    def __init__(self,x_pos,y_pos,filename,alt_filename, speed):
        '''
        Constructor
        '''
        Sprite.__init__(self,x_pos,y_pos,filename, alt_filename)
        self.speed = speed
        self.width = self.bitmap.get_width()
        self.height = self.bitmap.get_height()
    def move(self,  level):
        if self.x < (0 - self.width): # Moved off left edge of screen.
            self.x = 640
        elif self.x > 640:  # Moved off right edge of screen.
            self.x = (0 - self.width)
        else: 
         self.x -= self.speed + (level * 0.5 * self.speed)
         
class TimedMoveable(Moveable):
    '''
    classdocs
    '''
    
    def __init__(self, x_pos, y_pos, filename, alt_filename, speed, delay, locs):
        '''
        Constructor
        '''
        Moveable.__init__(self, x_pos, y_pos, filename, alt_filename, speed)
        if delay:
            self.delay = delay * 1000  #delay is in seconds, while self.delay needs to be msecs
            self.timer = time.get_ticks()
        self.locations = locs
    def move(self,  level):
        #determine if a change in location is needed (level is not used at present)
        if (self.timer + self.delay) < time.get_ticks():
         new_loc = random.choice(self.locations)
         self.x = new_loc[0]
         self.y = new_loc[1] 
         self.timer = time.get_ticks()
        
        #TODO add ability of crocs and flies to be on other moveables.

class RiverMoveable(TimedMoveable):
    '''
    classdocs
    '''
    
    def __init__(self, x_pos, y_pos, filename, alt_filename, speed, 
                 delay = None, locs = None):
        '''
        Constructor
        '''
        TimedMoveable.__init__(self, x_pos, y_pos, filename, alt_filename, 
                               speed, delay, locs)
        if delay:
            self.sinkable = True
        else:
            self.sinkable = False     # sinkable determines if object can sink
                                      # ie: is it a log or turtle.
        self.temp_bitmap = None
        self.timer = None
        self.sinking = False
    def move(self,  level):
        Moveable.move(self,  level)  #Recall the move function from Moveable
        if self.sinking == True and (self.timer + 4*self.delay) < time.get_ticks():#Have sunk so need to surface
            self.timer = None
            self.bitmap = self.temp_bitmap
            self.temp_bitmap = None
            self.sinking = False
            self.draw = True
    def sink(self):
        if self.timer == None:
            self.timer = time.get_ticks()
        if self.temp_bitmap == None:  # ensures this only happens once
            self.temp_bitmap = self.bitmap
            self.sinking = True
        if (self.timer + self.delay) < time.get_ticks(): #start to sink
            if self.bitmap != self.alt_bitmap:  
                self.bitmap = self.alt_bitmap
        if (self.timer + 2*self.delay) < time.get_ticks(): #Sunk
            self.draw = False
        
