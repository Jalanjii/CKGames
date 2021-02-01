import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
fric_cst = 0.01
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.fwrd = [0,0]
        self.orient = ""
        self.spin = False
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]+90,self.image_center[1]],
                              self.image_size,self.pos, self.image_size, self.angle)
                              
        else: 
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        
    def update(self):
        #position update
        self.pos[0] = (self.pos[0]+ self.vel[0])%WIDTH
        self.pos[1] = (self.pos[1]+ self.vel[1])%HEIGHT
        
        #forward vector:
        self.fwrd[0] = angle_to_vector(self.angle)[0]
        self.fwrd[1] = angle_to_vector(self.angle)[1]
        #thrust
        if self.thrust:
            self.vel[0] += self.fwrd[0]/7
            self.vel[1] += self.fwrd[1]/7
        #friction update
        self.vel[0] *= (1-fric_cst)
        self.vel[1] *= (1-fric_cst)
        #ship orientation    
        if self.spin:
            if self.orient == "right":
                self.angle += self.angle_vel
            elif self.orient == "left":
                self.angle -= self.angle_vel          
            else:
                self.angle = self.angle
    
    def angvelinc(self, spin):    #this version has more flexibility if you want to 
        self.angle_vel = 0.07	  #have asymmetrical angular velocity,
        self.orient = "right"
        self.spin = spin
        
    def angveldec(self, spin):
        self.angle_vel = 0.07
        self.orient = "left"
        self.spin = spin
                
    def thruster(self, thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 10 * forward[0], self.vel[1] + 10 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
     
    def get_radius(self):
        return self.radius
    def get_position(self):
        return self.pos
              
        
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):                                  
        if self.animated:
            sub_exp_index = (self.age % 20) // 1
            sub_exp_center = [self.image_center[0] + sub_exp_index * self.image_size[0],
                          self.image_center[1]]
            canvas.draw_image(self.image, sub_exp_center,
                              self.image_size, self.pos, self.image_size)
                          
        
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 2
        
        if self.age > self.lifespan:
            return True
        else:
            return False
        
    def get_radius(self):
            return self.radius
    
    def get_position(self):
        return self.pos
    
    def collide(self, other_object):
        if (dist(self.pos, other_object.get_position())-(self.radius+other_object.get_radius()))<0:
            return True
        else: return False
            
def key_handlerd(key): 
    
    if key == simplegui.KEY_MAP['left']:
        my_ship.angveldec(True)
            
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angvelinc(True)
        
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thruster(True)
        
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
    
def key_handleru(key): 
    if key == simplegui.KEY_MAP['up']:
        my_ship.thruster(False)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angveldec(False)
            
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angvelinc(False)
        
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()
        
def draw(canvas):
    
    global time, started, lives, score
    
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text("Lives: "+str(lives), [50, 50], 22, "White")
    canvas.draw_text("Score: "+str(score), [680, 50], 22, "White")
    score += group_group_collide(rock_group, missile_group)
    
    if group_collide(rock_group, my_ship):
        lives -= 1
    if lives == 0:
        started = False
        
    my_ship.draw(canvas)   
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    my_ship.update()

    if not started:
        rock_group.difference_update(rock_group)
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())     
    else:
        process_sprite_group(canvas, rock_group)
        
def rock_spawner():
    global score
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    if dist(rock_pos, my_ship.get_position()) < 75:
        rock_pos = [random.randrange(0, WIDTH)+90, random.randrange(0, HEIGHT)] #85=(rock_radius*2)+10
    rock_vel = [random.random() * .2*score - .3, random.random() * .2*score - .3]
    rock_avel = random.random() * .2 - .1
    if len(rock_group) <= 12:
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        
def process_sprite_group(canvas, a_set):
    for sprt in set(a_set):
        sprt.draw(canvas)
        if sprt.update():
            a_set.remove(sprt)
def group_collide(group, other_object):
    Tag = False
    for st in set(group):
        if st.collide(other_object):
            Tag = True
            group.remove(st)
            a_explosion = Sprite(st.pos, st.vel, st.angle, st.angle_vel,
                                 explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_explosion)
            
    return Tag

def group_group_collide(group_1, group_2):
    discard = set([])
    count = 0
    for g1 in set(group_1):
        if group_collide(group_2, g1):
            count += 1
            discard.add(g1)
    group_1.difference_update(discard)
    return count

    
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
missile_group = set([])
rock_group = set([])
explosion_group = set([])

frame.set_draw_handler(draw)
frame.set_keydown_handler(key_handlerd)
frame.set_keyup_handler(key_handleru)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

timer.start()
frame.start()
