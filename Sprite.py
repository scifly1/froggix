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

class Sprite:
    '''
    classdocs
    '''


    def __init__(self,x_pos,y_pos,filename, alt_filename):
        '''
        Constructor
        '''
        self.x, self.y =  x_pos, y_pos
        self.bitmap = image.load(filename)
        if alt_filename:
            self.alt_bitmap = image.load(alt_filename)
        else:
            self.alt_bitmap = None
        self.draw = True
    def render(self,screen):
        if self.draw:
            screen.blit(self.bitmap, (self.x,self.y))

