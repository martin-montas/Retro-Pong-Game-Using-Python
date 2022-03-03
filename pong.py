#  Coder: Martin Montas
#  Date:`date +%d/%m/%y`
#  Email:martinmontas@gmail.om
#  Breif Description :     pong game using pygame                       
#  Detailed Description : almost DONE

import pygame
import sys



pygame.init()

#colors for the objects
white = (255,255,255)
black = (0,0,0)

#frames per minutes
fps = 60

#how far you want the paddles
far = 32
pad_width = 15
pad_height = 60

#screen width and height
score_value = 0
screen_width = 400 
screen_height = 400
hit = pygame.mixer.Sound("270326__littlerobotsoundfactory__hit-01.ogg")     #this is the screen width and height of the game
hit.set_volume(0.08)
screen = pygame.display.set_mode((screen_width,screen_height))              #this is where the object get displayed

#score numbers coordinates of the lest paddle
textx1 = screen_width/2
texty1 = 10 

#score numbers coodinates of the right paddle
score_value2 = 0
textx2 = screen_width/2 -25
texty2 = 10
clock = pygame.time.Clock()
pygame.display.set_caption("Xxxpong gamexxX")


class pong:
    #this is the main class that creates paddles for the game with its atributes and variables
    def __init__(self,top,left,width,height,play_change,score):
        self.top = top          #this is the x coordinate
        self.left = left        #this is the y coordinate
        self.width = width
        self.height = height
        self.background_color = (0,0,0)
        self.play_change = play_change 
        self.bottom = self.left + self.height
        self.font = pygame.font.Font("freesansbold.ttf",20)
        self.score = score
        self.display_score = self.font.render("Score: %d " % (self.score), True, white)
        self.color = (255,255,255)


    def play_changes(self,dt):
        #here the paddles moves
        yCoordinate = self.left + (self.play_change * dt)
        if yCoordinate <= 0:
            return
        if yCoordinate + self.height >= screen_height:
            return
        self.left = yCoordinate

class ball:
    def __init__(self,b_left,b_top,b_height,b_width):
        #this is the x coordinate
        self.b_left = b_left
        #this is the y coordinate 
        self.b_top = b_top          
        self.b_width = b_width
        self.b_height = b_height
        self.move_x = 250
        self.move_y = 250

    def ball_act(self,dt):
        #this makee the ball move
        self.b_top  += self.move_x * dt
        self.b_left += self.move_y * dt

    def ball_bound(self):
        # this bound the ball to the wall
        if (self.b_left < 0) or (self.b_left > screen_height - 10):
            hit.play()
            self.move_y *= -1 
        if (self.b_top < 0) or (self.b_top > screen_width - 10):
            hit.play()
            self.move_x *= -1

    def collide(self,col_p,col_b,col_p2):
        #this helps the paddles collide with the ball
        collision_tolerance = 5
        if col_b.colliderect(col_p):  
            if (abs(col_p.top - col_b.bottom) < collision_tolerance) and (self.move_y < 0):
                self.move_y  *= -1 
            if (abs(col_p.bottom - col_b.top) < collision_tolerance) and (self.move_y > 0):
                self.move_y *= -1  
            if (abs(col_p.right - col_b.left) < collision_tolerance) and (self.move_x > 0):
                self.move_x *= -1 
            if (abs(col_p.left - col_b.right) < collision_tolerance) and (self.move_x < 0):
                self.move_x *= -1 
        if col_p.colliderect(col_p2):  
            if (abs(col_p.top - col_p2.bottom) < collision_tolerance) and (self.move_y < 0):
                self.move_y  *= -1 
            if (abs(col_p.bottom - col_p2.top) < collision_tolerance) and (self.move_y > 0):
                self.move_y *= -1  
            if (abs(col_p.right - col_p2.left) < collision_tolerance) and (self.move_x > 0):
                self.move_x *= -1 
            if (abs(col_p.left - col_p2.right) < collision_tolerance) and (self.move_x < 0):
                self.move_x *= -1 

#here goes the instantiation of the classes
play = pong(far,abs(screen_height/2),pad_width,60,0,0)
play_t = pong((screen_width - far)- pad_width,abs(screen_height/2),pad_width,60,0,0) 
n_ball = ball(screen_width/2,screen_width/2,15,15)
middle = pong(screen_width/2,0,1,screen_height,0,0)

while True:
    ## main loop
    dt = clock.tick(fps) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_w:
                play.play_change = -200
            if event.key == pygame.K_s:
                play.play_change = 200

            if event.key == pygame.K_UP:
                play_t.play_change = -200
            if event.key == pygame.K_DOWN:
                play_t.play_change = 200

        if event.type == pygame.KEYUP:
            if event.key == (pygame.K_UP or pygame.K_DOWN):
                play_t.play_change = 0
            if event.key == (pygame.K_s or pygame.K_w):
                play.play_change = 0


    #here i draw the shapes with the objects atributes
    screen.fill(black)
    col_p = pygame.draw.rect(screen,white,(play.top,play.left,play.width,play.height))
    col_p2 = pygame.draw.rect(screen,white,(play_t.top,play_t.left,play_t.width,play_t.height))
    col_b = pygame.draw.rect(screen,white,(n_ball.b_top, n_ball.b_left,n_ball.b_height,n_ball.b_width))
    pygame.draw.rect(screen, white,(middle.top,middle.left,middle.width,middle.height))

    #class functions
    n_ball.ball_bound()
    n_ball.ball_act(dt)
    play.play_changes(dt)
    play_t.play_changes(dt)
    n_ball.collide(col_b,col_p,col_p2)

    #renders each paddle self.score on the object and actualize it    
    screen.blit(play.font.render(str(play.score), True, white), [textx1, texty1])
    screen.blit(play_t.font.render(str(play_t.score), True, white), [textx2, texty2])
    if col_b.x <= 0:
        play.score += 1
        del n_ball
        n_ball = ball(screen_width/2,screen_height/2,15,15)

    if col_b.x + n_ball.b_height >= screen_width:
        play_t.score += 1
        del n_ball
        n_ball = ball(screen_width/2,screen_height/2,15,15)
    pygame.display.flip()

