import pygame
from pygame import mixer
#from playsound import playsound
import tkinter as tk
from tkinter import *
import random

pygame.mixer.init()
pygame.font.init() #intializing the font

# global variables
s_width = 800
s_height = 700
play_width = 300  #300 // 10 = 30 width per block
play_height = 600  #600 // 20 = 30 height per block
block_size = 30
global row_no


top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(200,190,140), (255, 0, 0), (255,100,180), (255,0,230), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

class Piece(object):  
    #rows = 20  -> y
    #columns = 10  -> x
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 # number from 0-possible rotations

logo_img = pygame.image.load('0270d405cf775da.png')
win_bg_img = pygame.image.load('Tetris-Logo1.jpg')
tetris_bg_img = pygame.image.load('tetris-wallpaper.jpg')
game_over_img = pygame.image.load('game_over.png')
help_img = pygame.image.load('help.png')
start_img = pygame.image.load('restart.png')
exit_img = pygame.image.load('exit_button.png')

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, win):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        win.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

#logo_button = Button(40, 50, logo_img, 0.5)
logo_button = Button(110, 90, logo_img, 1.5)
win_bg_button = Button(285, 5, win_bg_img, 0.35)
tetris_bg = Button(-10, 0, tetris_bg_img, 1.15)
game_over_button = Button(220, 350, game_over_img, 0.6)
help_button = Button(60, 170, help_img, 0.2)
start_button = Button(50, 300, start_img, 0.5)
exit_button = Button(50, 450, exit_img, 0.5)

#home = pygame.image.load('homeBtn.png')
#home_btn = Button(home, (24,24), s_width - 750, s_height/2 - 100)

def create_grid(locked_pos={}):  
    #we basically represent the grid as a list full of colors
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
    #the sublist represents the 10 colors - 10 squares in each row, the outer list is number of rows
    #We will create a multidimensional list that contains 20 lists of 10 elements (rows and columns). 
    #Each element in the lists will be a tuple representing the color of the piece in that current position. 
    
    #we are going to draw the grid by looping through through the 'grid'
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos: #static positions, j=col, i=row
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid
#The locked position parameter will contain a dictionary of key value pairs where each key is a position of a piece that has already fallen and each value is its color. 
# We will loop through these locked positions and modify our blank grid to show these pieces.

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] 
    #shape.rotation % len(shape.shape) - for getting the sublist

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] #[[()], [()]] - embedded list
    accepted_pos = [j for sub in accepted_pos for j in sub] #[(), ()] - overidding

    formatted = convert_shape_format(shape) #[(), ()]

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: 
            #we wnat our shape to fall from the top of the screen, but we dont want the rest of the shape to appear on the top of the screen
                return False
    return True
#When we are moving and rotating our shape we need to make sure that it is moving into a valid space. 
# We are going to use the valid_space() function to check this. 
# This function will have two parameters: grid and shape. 
# We will check the grid to ensure that the current position we are trying to move into is not occupied. We can do this by seeing if any of the positions in the grid that the shape is attempting to move into have a color. 
# If they have a color other than black than that means they are occupied, otherwise they are free.

def check_lost(positions): 
    #are any of the shapes above the screen - then indicate the player lost
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("couriernew", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (235,245,255), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (235,245,255), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0 #increment
    for i in range(len(grid)-1, -1, -1): #loops thorugh the grid backwards
        row = grid[i]
        if (0,0,0) not in row:
        #if there is no black space i.e its is completely filled with objects then clear the row 
            inc += 1 #whenver we delete a row we add one to the increment
            ind = i #indicates how many row the previous line has to move down
            
            for j in range(len(row)):
            #get every position in the row, i is gonna stay static since we are already in the curent row
                try:
                    del locked[(j,i)]
                except:
                    continue
            #every other row has to move down and add other row on the top
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc) #add y value to shift it down
                locked[newKey] = locked.pop(key) #the last color value will be equal to the new position

    count = 0
    row_no = inc
        
    #pygame.mixer.Sound('C:\users\ vinny\Downloads\D6Y2KAX-casino-bling.mp3')
    #pygame.mixer.music.play(loops=0)

    if row_no == 2:
        #playsound('C:\Users\vinny\Downloads\D6Y2KAX-casino-bling.mp3')
        draw_text_middle(win, 'DOUBLE!', 80, (255,255,100))
        pygame.display.update()
        pygame.time.delay(1500)
    elif row_no == 3:
        draw_text_middle(win,'TRIPLE!', 80, (255,255,100))
        pygame.display.update()
        pygame.time.delay(1500)
    elif row_no == 4:
        count += 1
        draw_text_middle(win, 'TETRIS!', 80, (255,255,100))
        pygame.display.update()
        pygame.time.delay(1500)
        while(count == 2):
            draw_text_middle(win, 'BACK-TO-BACK TETRIS!', 80, (255,255,100))
            pygame.display.update()
            pygame.time.delay(1500)
    count = 0
    
    return inc  #how many rows we ended up clearing

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('couriernew', 30, bold = True)
    label = font.render('Next Shape', 1, (0,0,100))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]  #we want the intial shape

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            
            pygame.draw.rect(surface, (0,0,0), (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
            for x in range(len(row)):
                pygame.draw.line(surface, (235,245,255), (sx, sy + x*block_size), (sx+150, sy+ x*block_size))
                for j in range(len(row)):
                    pygame.draw.line(surface, (235,245,255), (sx + j*block_size, sy),(sx + j*block_size, sy + 150))
            

    surface.blit(label, (sx - 10, sy - 50))

def draw_window(surface, grid, score=0):
    surface.fill((165,137,193))
    # Tetris Title
    win_bg_button.draw(surface)
    pygame.font.init()
    font = pygame.font.SysFont('constantia', 70)
    label = font.render('TETRIS!', 1, (0,0,100))
    #surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 20))

    #Buttons
    '''startButton = tk.Button(height=2, width=9,background='yellow',foreground='black',font=('Coolvetica Rg',20),text="Start",command=)
    startButton.pack()
    startButton.place(x=200,y=150)'''
    #exitButton = tk.Button(height=2, width=9,background='yellow',foreground='black',font=('Coolvetica Rg',20), text="Exit", command = destroy)
    #exitButton.pack()
    #exitButton.place(x=200,y=170)
    
    # current score
    font = pygame.font.SysFont('couriernew', 30, bold = True)
    label = font.render('Score: ' + str(score), 1, (0,0,100))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 3, sy + 180))
    
    #pygame.draw.rect(surface, (0,0,0), (sx + 60, sy + 60, ))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (235,245,255), (top_left_x - 9, top_left_y - 9, play_width + 15, play_height + 9), 9)
    pygame.draw.rect(surface, (235,245,255), (sx - 5, sy - 6, play_width/2 + 10, play_height/4 + 10), 5)

    draw_grid(surface, grid)
    #pygame.display.update() 

def help():
    root = Tk()
    root.title('Help!')
    root.geometry('1900x1000')
    var1 = "Rules to play Ping Pong:"
    var2 = "To contol the paddle,"
    var3 =  " has to use Q ey for moving UP \n and A key for moving DOWN"
    var4 = "and "+ " has to use P key \n for moving UP and L for moving DOWN."
    splashLabel2 = Label(root, background='pink', font=("Helvetica", 18), text=var1)
    splashLabel2.pack()
    splashLabel2.place(x=650, y=350)
    splashLabel3 = Label(root,background='pink',font=("Helvetica", 18),text=var2)
    splashLabel3.pack()
    splashLabel3.place(x=0,y=380)
    splashLabel4 = Label(root,background='pink',font=('Helvetica', 18),text=var3)
    splashLabel4.pack()
    splashLabel4.place(x=0,y=420)
    splashLabel5 = Label(root, background='pink', font=('Helvetica', 18), text=var4)
    splashLabel5.pack()
    splashLabel5.place(x=850, y=420)
    splashLabel6 = Label(root,highlightthickness=5,height=2,width=5,background='white',font=('Helvetica',18),text="Q")
    splashLabel6.pack()
    splashLabel6.place(x=200,y=490)
    splashLabel7 = Label(root,highlightthickness=5, height=2, width=5, background='white', font=('Helvetica', 18), text="A")
    splashLabel7.pack()
    splashLabel7.place(x=200, y=550)
    splashLabel8 = Label(root,highlightthickness=5,height=2,width=5,background='white',font=('Helvetica',18),text="P")
    splashLabel8.pack()
    splashLabel8.place(x=1200,y=490)
    splashLabel9 = Label(root,highlightthickness=5,height=2,width=5,background='white',font=('Helvetica',18),text="L")
    splashLabel9.pack()
    playButton = tk.Button(root,height=2,width=9,background='yellow',font=('Helvetica',18),text="Play",command=main)
    playButton.pack()
    playButton.place(x=700,y=550)
    

def main(win): 
    #last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:

        #Background Sound
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() #this gets how long the while loop took to run
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 4: #every 4 seconds we are going to increase the speed
            level_time = 0
            if level_time > 0.15:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1 #automatically move the piece down
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            
            if help_button.draw(win):
                help()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

                
        shape_pos = convert_shape_format(current_piece)
        #check all positions of the piece if we have to hit the ground or lock it

        #adding piece to the the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i] #current iteration
            if y > -1: #we are not above the screen
                grid[y][x] = current_piece.color

        #if piece hits the ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        #if start_button.draw(win):
            #run = False
        
        if start_button.draw(win):
            run = False
        if exit_button.draw(win):
            pygame.display.quit()
        pygame.display.update()

        #Checks if user lost
        if check_lost(locked_positions):
            game_over_button.draw(win)
            pygame.display.update()
            mixer.music.load('C:\Users\vinny\Downloads\D6Y2KAX-casino-bling.mp3')
            mixer.music.play(loops = 0)
            draw_text_middle(win, "G A M E  O V E R", 60, (255,255,100))
            pygame.time.delay(1500)
            #playsound('C:\Users\vinny\Downloads\D6Y2KAX-casino-bling.mp3')
            run = False
    

def main_menu(win):  
    run = True
    while run:
        win.fill((255,255,100))
        #tetris_bg.draw(win)
        logo_button.draw(win)
        pygame.font.init()
        font = pygame.font.SysFont('constantia', 120)
        label = font.render('TETRIS!', 1, (0,0,100))
        #pygame.draw.rect(win, (0,0,0), (top_left_x-250 ,top_left_y+500, s_width , s_height/4), 0)
        #win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 250))
        
        '''if start_button.draw(win):
            main(win)
        if exit_button.draw(win):
            run = False'''
        
        font = pygame.font.SysFont('couriernew', 40, bold = True)
        label = font.render('Press Any Key To Play!', 1, (0,0,100))

        win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 500))
        #draw_text_middle(win, 'Press Any Key To Play', 40, (165,137,193))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    
    #home_btn.draw(win)
    #pygame.dispaly.update()
    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)