'''

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

