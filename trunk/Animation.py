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

class Animation():
    '''
    classdocs
    '''


    def __init__(self, frames, delay, loop = False):
        '''
        Constructor
        '''
        #list of surfaces that cycle to form the animation
        self.frames = [image.load(frame) for frame in frames] 
        self.delay = delay # in milliseconds
        self.counter = -1
        self.loop = loop
        self.timer = None
        
    def run(self, x_pos, y_pos):
        self.timer = time.get_ticks()
        self.x, self.y = x_pos, y_pos
        self.counter = 0        
        
    def update(self, screen):
        if self.timer != None:
            if (self.timer + self.delay) < time.get_ticks():
                self.counter += 1
                self.timer = time.get_ticks()
            
                if self.counter > len(self.frames) and self.loop == True:
                    self.counter = 0
                elif self.counter >= len(self.frames) and self.loop == False:
                    self.counter = -1
                    self.timer = None
        
        if self.counter >= 0:
                    screen.blit(self.frames[self.counter],(self.x,self.y))
        
        
        
            
        