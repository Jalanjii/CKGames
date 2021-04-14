
import simplegui
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ballacc = .10
padvelrate = 2

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1, 0]


def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]
    if direction == LEFT:
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]
    
    
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  
    global score1, score2 
    spawn_ball(LEFT)
    paddle1_pos = float(HEIGHT / 2)
    paddle1_vel = float(0)
    paddle2_pos = float(HEIGHT / 2)
    paddle2_vel = float(0)
    score1 = 0
    score2 = 0
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
     
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] <= -1 + BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT:
        if paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
             paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT:
        if paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
             paddle2_pos += paddle2_vel
        
        
        
    
    canvas.draw_line((HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), 
                     (HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), 8, 'White')
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                     [WIDTH - HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    
    
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:#left
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] += ball_vel[0] * ballacc
            ball_vel[1] += ball_vel[1] * ballacc
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
    if ball_pos[0]  >= WIDTH - BALL_RADIUS - PAD_WIDTH:#right
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] += ball_vel[0] * ballacc
            ball_vel[1] += ball_vel[1] * ballacc
        else:
            score1 += 1
            spawn_ball(LEFT)
            
            
    canvas.draw_text(str(score1), [200,100], 30, "White")
    canvas.draw_text(str(score2), [380,100], 30, "White")
 
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
        paddle1_vel += padvelrate
    elif key == simplegui.KEY_MAP['up']:
        paddle1_vel -= padvelrate
    elif key == simplegui.KEY_MAP['s']:
        paddle2_vel += padvelrate
    elif key == simplegui.KEY_MAP['w']:
        paddle2_vel -= padvelrate
    else:
        key = ' '
           
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
        paddle1_vel -= padvelrate
    elif key == simplegui.KEY_MAP['up']:
        paddle1_vel += padvelrate
    elif key == simplegui.KEY_MAP['s']:
        paddle2_vel -= padvelrate
    elif key == simplegui.KEY_MAP['w']:
        paddle2_vel += padvelrate
    else:
        key = ' '
        
        
def restart():
    new_game()
    
    
def stop():
    frame.stop()

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Replay', restart)
frame.add_button('Exit', stop, 60)


new_game()
frame.start()
