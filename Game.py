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

from Moveable import *
from Home import Home
from Locations import Locations
from Animation import Animation


class Game():
    
    def __init__(self,no_of_lives = 4, score = 0):
        
        #Setup some Game constants
        self.GAME_LENGTH = 60000.0  # 60 seconds
        self.GAME_TIME_BONUS = 1000 #maximum points available as time bonus points
        self.FLY_POINTS = 100
        self.HOME_POINTS = 250
        self.MOVE_POINTS = 10
        
        #Create frogs and other objects and package them in lists
        frog_x_positions = [x*50 for x in range(no_of_lives) ]
        self.frogs = [Moveable(x,430,'data/frog.png', 'data/splat.png', 0) for x in frog_x_positions ]
        self.frog = self.frogs[0]  
        self.frog.x,  self.frog.y = 305, 405 
        
        cars = [Moveable(x,300,'data/car.png',None, 3) for x in range(0,640,213)]
        lorries = [Moveable(x,350,'data/blue-lorry.png', None,2) for x in [200,520]]
        bikes = [Moveable(x,250,'data/bike.png',None,  7) for x in [300,620]]
        
        self.vehicles = []
        self.vehicles.extend(cars)
        self.vehicles.extend(lorries)
        self.vehicles.extend(bikes)
        
        logs1 = [RiverMoveable(x, 50, 'data/log.png', None, -4) for x in [0, 128, 256,384,512]]
        turtles = [RiverMoveable(x, 100, 'data/turtle.png', 'data/sink_turtle.png', 2, 0.75)\
                    for x in [50, 178, 306,434,562]]
        logs2 = [RiverMoveable(x, 150, 'data/log.png', None, -4) for x in [0, 128, 256,384,512]]
        self.river_objects = []
        self.river_objects.extend(logs1)
        self.river_objects.extend(turtles)
        self.river_objects.extend(logs2)
        
        bank_locations = [Locations(x,y) for (x,y) in [(210, 15), (360, 15), 
                                                       (510, 15), (50, 15), (70, 215), 
                                                       (220, 215), (380, 215), (530, 215), 
                                                       (200, 415), (440, 415)]]
        self.homes = [Home(x, 0) for x in [50, 200, 350, 500]]
        
        self.fly_locations = []
        self.fly_locations.extend(bank_locations)
        
        self.croc_locations = self.homes
        self.croc_locations.append(Locations(-50,-50)) # Add an offscreen location
        
        self.flies = [TimedMoveable(x, 15, 'data/fly.png', None, None,  1.5, self.fly_locations)\
                  for x in [210, 360, 510]]
        self.crocs = [TimedMoveable(50, 0, 'data/croc.png', None, None,  3, self.homes)]
        
        splash = ['data/splash1.png','data/splash2.png','data/splash3.png']
        self.animations = [Animation(splash,150)]
    
        self.score = score
        self.no_of_lives = no_of_lives
        '''game_data = {'frog':frog,'frogs':frogs, 'vehicles':vehicles, 'river_objects':river_objects,\
                      'homes':homes, 'flies':flies, 'crocs':crocs,  'score':score ,'anims':animations }
        return game_data
    '''

    