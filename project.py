import pygame
from pygame import mixer
from playsound import playsound
import tkinter as tk
from tkinter import *
import random

pygame.mixer.init()
pygame.font.init() #intializing the font

# global variables
s_width = 800
s_height = 600
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

keys_img = pygame.image.load('C:/Users/Vinny/Downloads/Keys.png.jpeg')
score_img = pygame.image.load('C:/Users/vinny/Pictures/Saved Pictures/ten-points.png')
rules_img = pygame.image.load('C:/Users/Vinny/Downloads/Instructions.png.jpeg')
#rules_img = pygame.image.load('icons8-tetris-64.png')
star_img = pygame.image.load('C:/Users/Vinny\Downloads/Four_lines_cleared.png.jpeg')
logo_img = pygame.image.load('C:/Users/Vinny\Pictures/Saved Pictures/0270d405cf775da (1).png')
win_bg_img = pygame.image.load('C:/Users/Vinny/Downloads/Tetris_title.png.jpeg')
#tetris_bg_img = pygame.image.load('tetris-wallpaper.jpg')
game_over_img = pygame.image.load('C:/Users/vinny/Pictures/Saved Pictures/Game-Over-Yellow-Transparent-PNG (1).png')
help_img = pygame.image.load('C:/Users/vinny/Pictures/Saved Pictures/18436.png')
restart_img = pygame.image.load('C:/Users/vinny/Pictures/Saved Pictures/303-3039460_reset-button-clipart.png')
start_img = pygame.image.load('C:/Users/Vinny/Downloads/start_gamepng.jpeg')
exit_img = pygame.image.load('C:/Users/Vinny/Downloads/exit_game.png.jpeg')

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
keys_button = Button(620, 280, keys_img, 0.27)
score_button = Button(630, 390, score_img, 0.2)
score_win_button = Button(620, 540, score_img, 0.5)
rules_button = Button(20, 90, rules_img, 1.0)
star_button = Button(50, 150, star_img, 1.0)
logo_button = Button(110, 90, logo_img, 1.5)
win_bg_button = Button(285, 5, win_bg_img, 0.35)
#tetris_bg = Button(-10, 0, tetris_bg_img, 1.15)
game_over_button = Button(220, 350, game_over_img, 0.6)
help_button = Button(720, 20, help_img, 0.1)
restart_button = Button(50, 300, restart_img, 0.5)
start_button = Button(290, 600, start_img, 0.5)
exit_button = Button(50, 450, exit_img, 0.5)

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
                    continue #every other row has to move down and add other row on the top
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc) #add y value to shift it down
                locked[newKey] = locked.pop(key) #the last color value will be equal to the new position
    row_no = inc
    #pygame.mixer.Sound('C:/Users/vinny/Downloads/eliminate_lines.mp3.mp3')
    #pygame.mixer.music.play(loops=1)

    if row_no == 2:
        #playsound('C:/Users/vinny/Downloads/eliminate_lines.mp3.mp3')
        draw_text_middle(win, 'DOUBLE!', 80, (255,255,100))
        score_win_button.draw(win)
        pygame.display.update()
        pygame.time.delay(500)
    elif row_no == 3:
        draw_text_middle(win,'TRIPLE!', 80, (255,255,100))
        score_win_button.draw(win)
        pygame.display.update()
        pygame.time.delay(500)
    elif row_no == 4:
        draw_text_middle(win, 'TETRIS!', 80, (255,255,100))
        star_button.draw(win)
        pygame.display.update()
        pygame.time.delay(500)
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

def help(win):
    run = True
    while run:

        win.fill((255,255,100))
        #font = pygame.font.SysFont('constantia', 50)
        #label = font.render('Rules To Play TETRIS', 1, (0,0,100))
        #win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 50))
        rules_button.draw(win)
        font = pygame.font.SysFont('constantia', 20, bold = True)
        inst1 = font.render('''Tetris, is a widely recognised game of stacking Tetrominoes ''', 1, (0,0,100))
        win.blit(inst1, (top_left_x - 80 , 90))
        inst2 = font.render('''by strategically rotating, moving and dropping them thereby''', 1, (0,0,100))
        win.blit(inst2, (top_left_x - 80, 115))
        inst2 = font.render('''creating lines that fill the box horizontally without empty''', 1, (0,0,100))
        win.blit(inst2, (top_left_x - 80, 140))
        inst2 = font.render(''' spaces before it reaches the top. The player loses when the''', 1, (0,0,100))
        win.blit(inst2, (top_left_x - 80, 165))
        inst2 = font.render('''tetrominoes make it to top of the playing field.''', 1, (0,0,100))
        win.blit(inst2, (top_left_x - 80, 190))
        inst2 = font.render('''1. You can move tetrominoes using left and right keys,''', 1, (0,0,255))
        win.blit(inst2, (top_left_x - 220, 280))
        inst2 = font.render('''and rotate them in both directions using''', 1, (0,0,255))
        win.blit(inst2, (top_left_x - 220, 305))
        inst2 = font.render('''-> UP Key for clockwise rotation ''', 1, (0,0,255))
        win.blit(inst2, (top_left_x - 220, 330))
        inst2 = font.render('''-> Down Button Key for Soft Drop.''', 1, (0,0,255))
        win.blit(inst2, (top_left_x - 220, 355))
        keys_button.draw(win)
        inst2 = font.render('''2. When a line of blocks is created, the entire line''', 1, (255, 0, 230))
        win.blit(inst2, (top_left_x - 220, 420))
        inst2 = font.render('''disappears and +10 points are rewarded.''', 1, (255, 0, 230))
        win.blit(inst2, (top_left_x - 220, 445))
        score_button.draw(win)
        inst2 = font.render('''3. The upcoming pieces will be shown in the Next Shape section.''', 1, (255, 100, 10))
        win.blit(inst2, (top_left_x - 220, 510))
        
        if start_button.draw(win):
            main(win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
            row = clear_rows(grid, locked_positions)
            score += clear_rows(grid, locked_positions) * 2
            if row == 2:
                score += 10
            elif row == 3:
                score += 10
            elif row == 4:
                score += 40

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        
        if restart_button.draw(win):
            run = False
        if exit_button.draw(win):
            pygame.display.quit()
        pygame.display.update()

        #Checks if user lost
        if check_lost(locked_positions):
            game_over_button.draw(win)
            pygame.display.update()
            mixer.music.load('C:/Users/vinny/Downloads/eliminate_lines.mp3.mp3')
            mixer.music.play(loops = 1)
            draw_text_middle(win, "G A M E  O V E R", 60, (255,255,100))
            pygame.time.delay(1500)
            playsound('C:/Users/vinny/Downloads/eliminate_lines.mp3.mp3')
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
        if help_button.draw(win):
            help(win)

        font = pygame.font.SysFont('couriernew', 40, bold = True)
        label = font.render('Press Any Key To Play!', 1, (0,0,100))
        win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 500))
        font = pygame.font.SysFont('couriernew', 20)
        label = font.render('@TEAM-6, ECE-A', 1, (0,0,100))
        win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 650))
        #draw_text_middle(win, 'Press Any Key To Play', 40, (165,137,193))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)