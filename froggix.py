
from pygame import *
import random
import os
import cPickle
import operator

#Classes used in the Game are defined here

class Sprite:
    def __init__(self,x_pos,y_pos,filename, alt_filename):
        self.x, self.y =  x_pos, y_pos
        self.bitmap = image.load(filename)
        if alt_filename:
            self.alt_bitmap = image.load(alt_filename)
        else:
            self.alt_bitmap = None
        self.draw = True
    def render(self):
        if self.draw:
            screen.blit(self.bitmap, (self.x,self.y))


class Moveable(Sprite):
    def __init__(self,x_pos,y_pos,filename,alt_filename, speed):
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
    def __init__(self, x_pos, y_pos, filename, alt_filename, speed, delay, locs):
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
    def __init__(self, x_pos, y_pos, filename, alt_filename, speed, delay = None, locs = None):
        TimedMoveable.__init__(self, x_pos, y_pos, filename, alt_filename, speed, delay, locs)
        if delay:
            self.sinkable = True
        else:
            self.sinkable = False
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
        

class Home:
    def __init__(self, x_pos,  y_pos):
        self.x,  self.y = x_pos, y_pos
        self.width,  self.height = 45,  45

#Global constants
game_length = 60000.0  # 60 seconds
game_time_bonus = 1000 #maximum points available as time bonus points
fly_points = 100
home_points = 250
move_points = 10
fly_locations = ((210, 15), (360, 15), (510, 15), (50, 15), (70, 215), (220, 215), (380, 215), (530, 215), (200, 415), (440, 415))
croc_locations = ((50, 0), (200, 0), (350, 0), (500, 0))
highscorefile = "data/highscores.dat"
letter_list = ['_','A', 'B', 'C', 'D',  'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', \
              'U', 'V', 'W', 'X', 'Y', 'Z' ]
    
#Global Function definitions are defined here. 

def intersect(frogger, mover):
    if ((frogger.x + frogger.width - 5) > mover.x - 15) and (frogger.x + 5 < mover.x + mover.width -15 ) \
    and (frogger.y > mover.y - frogger.height) and (frogger.y < mover.y + mover.height  ):
        return mover
    else:
        return None

def nextFrog(game_data, lives,  init_lives,  drowned = False, crushed = False):
    if lives > 0:
         if crushed:
            game_data['frog'].bitmap = game_data['frog'].alt_bitmap
         if drowned:
             drowned_frog = [(index, value) for (index, value) in enumerate(game_data['frogs'])\
                                                                                       if  value == game_data['frog']]
             game_data['frogs'][drowned_frog[0][0]].draw = False
        
         frog = game_data['frogs'][init_lives-lives]  
         frog.x, frog.y = 305,405
    else:
        frog = None
    return frog 
    
def updateCountdown(start_time,  level_counter):
    time_now = time.get_ticks()
    game_left = (time_now - start_time) / (game_length - (level_counter * 10000))
    return game_left
    
def drawCountdown(game_left):
    x = 422
    width = 196  #original rect at 100%
    right = x + width  #right extent of countdown box
    
    game_left = 1 - game_left
    width *= game_left
    x = right - width
    
    rect = Rect(x,452, width,16)  
    screen.fill((220, 0, 0), rect)
    
def initGame(no_of_lives = 4 ,  score = 0):
    #Create frogs and other objects, package them in lists and return a dictionary of the lists.
    frog_x_positions = [x*50 for x in range(no_of_lives) ]
    frogs = [Moveable(x,430,'data/frog.png', 'data/splat.png', 0) for x in frog_x_positions ]
    frog = frogs[0]  
    frog.x,  frog.y = 305, 405 
    
    cars = [Moveable(x,300,'data/car.png',None, 3) for x in range(0,640,213)]
    lorries = [Moveable(x,350,'data/blue-lorry.png', None,2) for x in [200,520]]
    bikes = [Moveable(x,250,'data/bike.png',None,  7) for x in [300,620]]
    
    vehicles = []
    vehicles.extend(cars)
    vehicles.extend(lorries)
    vehicles.extend(bikes)
    
    logs1 = [RiverMoveable(x, 50, 'data/log.png', None, -4) for x in [0, 128, 256,384,512]]
    turtles = [RiverMoveable(x, 100, 'data/turtle.png', 'data/sink_turtle.png', 2, 0.75)\
                for x in [50, 178, 306,434,562]]
    logs2 = [RiverMoveable(x, 150, 'data/log.png', None, -4) for x in [0, 128, 256,384,512]]
    river_objects = []
    river_objects.extend(logs1)
    river_objects.extend(turtles)
    river_objects.extend(logs2)
    
    homes = [Home(x, 0) for x in [50, 200, 350, 500]]
    
    flies = [TimedMoveable(x, 15, 'data/fly.png', None, None,  1.5, fly_locations)\
              for x in [210, 360, 510]]
    crocs = [TimedMoveable(50, 0, 'data/croc.png', None, None,  3, croc_locations)]

    game_data = {'frog':frog,'frogs':frogs, 'vehicles':vehicles, 'river_objects':river_objects,\
                  'homes':homes, 'flies':flies, 'crocs':crocs,  'score':score }
    return game_data
    
def loadHighscores(): #returns a list of unpickled highscores or an empty list if no scores
    if os.path.exists(highscorefile):
        hsfile = open(highscorefile,  'r')
        highscores = cPickle.load(hsfile)
        hsfile.close()
        return highscores
    else:
        return []

def saveHighscores(highscores):
    hsfile = open(highscorefile,  'w')
    cPickle.dump(highscores, hsfile)
    hsfile.close()
    
def updateName(name, letter_list_index, Enter=False):
    split_name = list(name)
    if Enter:
        split_name.insert(-1, letter_list[letter_list_index])
    else:
        split_name.pop()
        split_name.append(letter_list[letter_list_index])
    name = ''.join(split_name)
    return name
   
def updateHighscores(name,  level_score):
    name = list(name)
    name.pop() # remove trailing _
    name = ''.join(name)
    highscores = loadHighscores()
    highscores.append((name, level_score))
    highscores.sort(key = operator.itemgetter(1),  reverse = True)
    if len(highscores) > 5:
        del highscores[5:]
    saveHighscores(highscores) 
    return highscores

#Game begins here.

#Set up pygame window.
mixer.pre_init(44100,-16,2, 1024)
init()
icon = image.load('data/icon.png')
display.set_icon(icon)
screen = display.set_mode((640,480))
display.set_caption('Froggix')

#Create font for text on screen
scorefont = font.Font(None, 40)
menufont = font.Font(None, 60)
titlefont = font.Font(None, 150)

#Create sound effect objects
splasheffect = mixer.Sound("data/splash.wav")
cheereffect = mixer.Sound("data/cheer.wav")
crasheffect = mixer.Sound("data/crash.wav")
cruncheffect = mixer.Sound("data/crunch.wav")
lickeffect = mixer.Sound("data/lick.wav")

#Load Music
mixer.music.load("data/Klonk.ogg")

#Start a new game
background = image.load('data/background.png')

mixer.music.play(-1)

game_data = initGame()
score = game_data['score']

#Set some constant text surfaces up
titletext = titlefont.render("Frogger!", True, (246, 230, 40))
playtext = menufont.render("Press 1 to Play",  True,  (246, 230,40))
quittext = menufont.render("Press Esc to Quit",  True, (246, 230, 40))
quittext1 = scorefont.render("Press Escape to quit or", True, (255, 0, 0))
quittext2 = scorefont.render("press Spacebar to try again", True, (255, 0, 0))
highscoretext = menufont.render("Highscores:",  True,  (255, 0, 0))
highscoretext1 = scorefont.render("a new Highscore!",  True, (255, 0, 0))
highscoretext2 = scorefont.render("Use the Up and Down keys to choose letters,",  True, (255, 0, 0))
highscoretext3 = scorefont.render("Enter to select and Backspace to delete.",  True, (255, 0, 0))


in_game = False  # a flag set when in play
titles = True  # a flag set when on Main title screen
game_over = False  # a flag set when on game_over screen
in_between_level = False # a flag set when between levels
reset = False  # flag set when game is reset at start of a new level
quit_screen = False #flag set to go to quit_screen
new_highscore = False # flag set when new highscore set
level_counter = 1
highscores = None
letter_list_index = 0
name = "_"

quit = 0

#Begin main game loop
while quit == 0:
    ti = time.get_ticks()
     
    screen.blit(background, (0,0))
    
    #Capture events.
    for e in event.get():
        if e.type == QUIT:
            quit = 1
        if e.type == KEYDOWN:
            if  e.key == K_1 and titles:
                titles = False
                reset = True
                in_game = True
            
            if e.key == K_ESCAPE:
                quit = 1
            if in_game:
                if e.key == K_UP and game_data['frog'].y > 20:
                    game_data['frog'].y -= 50
                    score += move_points
                if e.key == K_DOWN and game_data['frog'].y < 405:
                    game_data['frog'].y += 50
                if e.key == K_LEFT and game_data['frog'].x > 10:
                    game_data['frog'].x -= 50
                if e.key == K_RIGHT and game_data['frog'].x < 600:
                    game_data['frog'].x += 50
            elif (in_between_level or (quit_screen and not new_highscore) )and e.key == K_SPACE:
                reset = True
            if new_highscore:
                if e.key == K_UP:
                    letter_list_index += 1
                    if letter_list_index > len(letter_list) - 1:
                        letter_list_index = 0
                    name = updateName(name, letter_list_index)
                if e.key == K_DOWN:
                    letter_list_index -= 1
                    if letter_list_index < 0:
                        letter_list_index = len(letter_list) - 1
                    name = updateName(name, letter_list_index)
                if e.key == K_RETURN:
                    if letter_list_index == 0:
                        highscores = updateHighscores(name, level_score)
                        new_highscore = False
                    else:
                        name = updateName(name, letter_list_index, True)
                        letter_list_index = 0
                        name = updateName(name, letter_list_index)
                if e.key == K_BACKSPACE:
                    name = list(name)
                    if len(name) > 1:
                        del name[-2]
                    name = ''.join(name)
    
    if titles:
        screen.blit(titletext, (100, 75))
        screen.blit(playtext, (180, 260))
        screen.blit(quittext, (180, 310))
        
    if in_between_level:
        if game_left != 1:
            level_counter += 1  # counts  the level number.  Used to calc time for next level 
            time_bonus =  int(round((1- game_left) * game_time_bonus))
            game_left = 1 # prevents the time_bonus being added on every loop through here
            level_score = score + time_bonus
            
            if frogs_safe == 0: # setup new game
                game_data = initGame()
            else: 
                game_data = initGame(frogs_safe, level_score)  #init data for next level
            
        if frogs_safe > 0:    
            screen.fill((0, 0, 0))
            resulttext = scorefont.render("You got a " + str(time_bonus)  + " point time bonus!", True, (255, 0, 0))
            resulttext1 = scorefont.render("You got " + str(frogs_safe)  + " home!", True, (255, 0, 0))
            resulttext2 = scorefont.render("Press Spacebar to begin level " + str(level_counter) + "!", True, (255, 0, 0))

            screen.blit(resulttext,  (80, 150))
            screen.blit(resulttext1, (80, 200))
            screen.blit(resulttext2, (80, 250))
            
        else:
            quit_screen = True
            in_between_level = False
            
    if reset:
            start_time = time.get_ticks()  # reset timer
            lives = init_lives = len(game_data['frogs'])
            score = game_data['score']
            frogs_safe = 0
            in_game = True
            in_between_level = False
            quit_screen = False
            highscores = None
            new_highscore = False
            reset = False
            
    if quit_screen:
        screen.fill((0, 0, 0))
        
        while highscores == None:
            quittext = scorefont.render("You got " + str(level_score)  + " points!", True, (255, 0, 0))
            highscores = loadHighscores()
            lowest_score = None
            if highscores:
                if len(highscores) > 4:  # Allow 5 records
                    lowest_score = highscores[4][1]
            if level_score > lowest_score: # new highscore
                new_highscore = True
            4
        if new_highscore == False:
            highscore_name_list = [scorefont.render(i[0] , True,  (255, 0, 0)) for i in highscores]
            highscore_score_list = [scorefont.render(str(i[1]),  True,  (255, 0, 0)) for i in highscores]
            screen.blit(highscoretext,  (150,  0))
            for a in range(len(highscore_name_list)):
                screen.blit(highscore_name_list[a],  (100,  50 * (a +1)))
                screen.blit(highscore_score_list[a], (400, 50 * (a + 1)))
            screen.blit(quittext,  (80, 300))
            screen.blit(quittext1, (80, 350))
            screen.blit(quittext2, (80, 400))
        else:
            nametext = scorefont.render(name,  True,  (255, 0, 0))
            
            screen.blit(quittext,  (200, 100))
            screen.blit(highscoretext1, (220,  150))
            screen.blit(nametext, (220, 225))
            screen.blit(highscoretext2,  (20, 300))
            screen.blit(highscoretext3,  (20, 350))
            
        
        
        level_counter = 1
                
        
    if in_game:
       
        #Move all objects
        to_move = ['vehicles', 'river_objects', 'crocs', 'flies', 'frogs']
        for li in to_move:
            [obj.move(level_counter) for obj in game_data[li]]
        
        #Collision detection 
        eat = [intersect(game_data['frog'], e) for e in game_data['flies']]
        hit = [intersect(game_data['frog'], v) for v in game_data['vehicles']]
        safe = [intersect(game_data['frog'], l) for l in game_data['river_objects'] if l.draw]  
        croc_lunch = [intersect(game_data['frog'], c) for c in game_data['crocs']]
        home = [intersect(game_data['frog'], h) for h in game_data['homes']]
        
        #Logic that determines outcomes of collisions.
        eaten_fly = [(index, value) for (index, value) in enumerate(eat) if  value != None]
        if eaten_fly: # A fly has been eaten
            mixer.Sound.play(lickeffect)
            del game_data['flies'][eaten_fly[0][0]] #remove fly
            new_fly = TimedMoveable(50, 15, 'data/fly.png', None, True,  3, fly_locations)
            game_data['flies'].append(new_fly)  # add in a new fly
            score += fly_points
            
        river_obj = [s for s in safe if s != None]
        if river_obj:  # if a river object is landed on.
            game_data['frog'].speed = river_obj[0] .speed
            if river_obj[0].sinkable:  #Determines if obj can sink
                river_obj[0].sink()
        else:
            game_data['frog'].speed = 0
         #Frog in river section: so dies if not on an object.
        if (50 < game_data['frog'].y < 200) and game_data['frog'].speed == 0: 
             mixer.Sound.play(splasheffect)
             lives -= 1
             game_data['frog'] = nextFrog(game_data,  lives,  init_lives,  True,  False)
         
        if  [h for h in hit if h != None] :    # if a vehicle is hit.
             mixer.Sound.play(crasheffect)
             lives -= 1
             game_data['frog'] = nextFrog(game_data,  lives,  init_lives,  False,  True)
        if [cl for cl in croc_lunch if cl != None]:  #if a croc is hit
             mixer.Sound.play(cruncheffect)
             lives -= 1
             game_data['frog'] = nextFrog(game_data,  lives,  init_lives,  False,  True)
             
        home_occupied = [(index, value) for (index, value) in enumerate(home) if  value != None]
        if game_data['frog'] and game_data['frog'].y < 50 and not home_occupied:  # frog on the bank but not in a home
             lives -= 1
             game_data['frog'] = nextFrog(game_data,  lives,  init_lives,  True,  False)
            
        elif game_data['frog'] and game_data['frog'].y < 50 and home_occupied:  #  Frog safe at home, so next frog in play.
            mixer.Sound.play(cheereffect)
            score += home_points
            del game_data['homes'][home_occupied[0][0]] #remove home
            lives -= 1
            frogs_safe += 1
            game_data['frog']= nextFrog(game_data,  lives,  init_lives)
        
        
        if game_data['frog'] == None:   #Go to next level or end game
            in_between_level = True
            in_game = False
            
        
        #Draw all objects.  The order is important. frogs need to be on top of all but vehicles
        to_draw = [ 'river_objects', 'flies', 'crocs', 'frogs',  'vehicles']
        for li in to_draw:
            [obj.render() for obj in game_data[li]]
        
        #Draw score to screen
        scoretext = scorefont.render("Score: " + str(score), True, (220, 0, 0))
        screen.blit(scoretext, (5, 400))

        #Update countdown timer
        game_left = updateCountdown(start_time, level_counter)
    
        if game_left < 1:
            drawCountdown(game_left)
        else:
            in_between_level = True
            in_game = False
            # end of in_game 

    
    display.update()

    # Limit to 30 FPS
    elapsed = time.get_ticks()-ti
    if elapsed < 33:
        time.wait(33 - elapsed)


