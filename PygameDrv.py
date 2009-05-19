"""
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

"""

from pygame import *
import platform
import os

class PygameDrv():
    def __init__(self):
        #Set up pygame window.
        if platform.system() == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib' 
        
        mixer.pre_init(44100,-16,2, 1024)
        init()
        icon = image.load('data/icon.png')
        display.set_icon(icon)
        screen = display.set_mode((640,480))
        display.set_caption('Froggix')
        
        #Create font for text on screen
        self.scorefont = font.Font(None, 40)
        self.menufont = font.Font(None, 60)
        self.titlefont = font.Font(None, 150)
        
        #Create sound effect objects
        self.splasheffect = mixer.Sound("data/splash.wav")
        self.cheereffect = mixer.Sound("data/cheer.wav")
        self.crasheffect = mixer.Sound("data/crash.wav")
        self.cruncheffect = mixer.Sound("data/crunch.wav")
        self.lickeffect = mixer.Sound("data/lick.wav")
        
        #Load Music
        mixer.music.load("data/Klonk.ogg")
        
        #Start a new game
        background = image.load('data/background.png')
        
        mixer.music.play(-1)
        
        '''
        game_data = initGame()
        score = game_data['score']
        '''
        