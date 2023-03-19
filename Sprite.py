import pygame, Path, random

sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()

ball_list = []

G_basket_hole = None

score = 0

class Sprite(pygame.sprite.Sprite):

    def __init__(self, image_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        sprites.add(self)
        pass
    
    def update(self):
        pass

    def get_pos(self):
        return self.rect.center

class Background(Sprite):

    background_x = 0
    background_y = 0

    vertical_delta = .7
    horizontal_delta = .5

    screen = None

    def __init__(self, image_path, start_pos_x, start_pos_y , screen):
        super().__init__(image_path, start_pos_x, start_pos_y)
        self.screen = screen

        self.background_x = start_pos_x
        self.background_y = start_pos_y
        pass

    def update(self):
        if self.background_x < self.screen.get_width()+67:
            self.background_x += self.vertical_delta
        else:
            self.background_x = 0
            pass

        if self.background_y < self.screen.get_height():
            self.background_y += self.horizontal_delta
        else:
            self.background_y = 0
            pass

        self.rect.center = [self.background_x, self.background_y]
        pass

    pass

class Healt_Bar(Sprite):

    healt = 0

    def __init__(self, image_path, pos_x, pos_y):
        super().__init__(image_path, pos_x, pos_y)
        self.healt = 3
        pass

    def damage(self):
        self.healt -= 1
        self.change_sprite(self.healt)
        print(self.healt)
        pass

    def change_sprite(self, inx):
        match inx:
            case 3:
                self.image = pygame.image.load(Path.healt_bar_3)
                pass

            case 2:
                self.image = pygame.image.load(Path.healt_bar_2)
                pass
                
            case 1:
                self.image = pygame.image.load(Path.healt_bar_1)
                pass

            case 0:
                self.image = pygame.image.load(Path.healt_bar_0)
                pass
        pass

class Hole(Sprite):
    
    pos_y = 0
    pos_x = 0
    screen = None

    acceleration = 0
    speed = 0
    is_pressed = False

    MAX_SPEED = 6

    def __init__(self, image_path, pos_x, pos_y, screen):
        global G_basket_hole
        super().__init__(image_path, pos_x, pos_y)
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.screen = screen
        G_basket_hole = self
        pass

    def update(self):
        self.move_horizontal()

        self.speed += self.acceleration

        if self.speed > self.MAX_SPEED:
            self.speed = self.MAX_SPEED
        if self.speed < -self.MAX_SPEED:
            self.speed = -self.MAX_SPEED

        if self.is_pressed == False and self.speed < 0:
            self.speed += .1
        elif self.is_pressed == False and self.speed > 0:
            self.speed -= .1
        
        if self.is_pressed == False:
            if abs(self.speed) <= .0000001:
                self.speed = 0


    def move_horizontal(self):
        if self.rect.x > self.screen.get_width():
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = self.screen.get_width()
        
        #value = pygame.math.lerp(self.rect.center[0], self.pos_x, self.t)

        self.rect.x += self.speed
        pass

    def go_right(self):
        self.is_pressed= True
        self.pos_x += 2
        self.acceleration = .5
        pass

    def go_left(self):
        self.is_pressed= True
        self.pos_x -= 2
        self.acceleration = -.5
        pass
    
    def un_press(self):
        self.is_pressed = False
        self.acceleration = 0
        pass

class Hole_Child(Sprite):

    hole = None
    vertical_offset = 0

    def __init__(self, image_path, pos_x, pos_y, main_hole, offset):
        super().__init__(image_path, pos_x, pos_y)
        global hole

        self.hole = main_hole
        self.vertical_offset = offset
        pass

    def update(self):
        self.rect.center = [self.hole.get_pos()[0] + self.vertical_offset, self.hole.get_pos()[1]]
        pass

class Second_Hole(Sprite):
    basket_hole = None

    def __init__(self, image_path, pos_x, pos_y, basket_hole):
        super().__init__(image_path, pos_x, pos_y)
        self.basket_hole = basket_hole
        pass

    def update(self):
        if self.basket_hole != None:
            self.rect = self.basket_hole.rect # tuple((self.basket_hole.rect[0] + 17, self.basket_hole.rect[1] + 57))
            self.rect = self.rect.move(17, 57)
            pass
        pass



class Ball(Sprite):

    healt_bar = None
    screen = None

    speed_vertical = 0
    align_x_axis = False

    scored =  False

    def __init__(self, image_path, pos_x, pos_y, healt_bar, screen):
        global balls
        super().__init__(image_path, pos_x, pos_y)

        balls.add(self)
        ball_list.append(self)

        self.healt_bar = healt_bar
        self.screen = screen

        ball_list.remove(self)
        ball_list.append(self)

        global score

        self.align_x_axis = False
        self.rect.x = self.random(0, self.screen.get_width())
        self.rect.y = -300 * (ball_list.index(self) + 1)
        self.speed_vertical = 3
        self.scored = False
    pass

    def update(self):
        
        if self.rect.y > self.screen.get_height() + 20:
            self.respawn()
        pass
        
        self.rect.y += self.speed_vertical

        if self.align_x_axis and self.scored == False:
            self.rect.x = G_basket_hole.rect.x
            self.rect = self.rect.move(27,0)
            if self.rect.y > 340:
                self.scored = True
                self.align_x_axis = False
    pass
    
    def respawn(self):
        balls.remove(self)
        balls.add(self)

        global score

        if self.scored == False:
            self.healt_bar.damage()
            print("asdasf")
        else:
            score += 1
            pass

        self.align_x_axis = False
        self.rect.x = self.random(0, self.screen.get_width())
        self.rect.y = -300 * (balls.has(self) + 1)
        self.speed_vertical = 3
        self.scored = False
    pass
    
    def enter_collider(self):
        self.align_x_axis = True
        self.speed_vertical = 2
        pass

    def exit_collider(self):
        self.align_x_axis = False
        self.speed_vertical = 3
        pass

    def random(self, start_val, end_val):
        return random.randrange(start_val, end_val)