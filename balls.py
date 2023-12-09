import random

import pygame


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = "lightskyblue3"
        self.text = text
        self.txt_surface = myfont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.text = ''
                self.txt_surface = myfont.render(self.text, True, self.color)
                self.draw(window)
            else:
                self.active = False
            self.color = 'dodgerblue2' if self.active else "lightskyblue3"
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = myfont.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Ball(pygame.sprite.Sprite):
    def __init__(self, r, bx, by, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.r = r
        self.vx = vx
        self.vy = vy
        randc = random.randint(1, 6)
        if randc == 1:
            self.image = pygame.image.load('ball_colors/ball_blue.png').convert_alpha()
        elif randc == 2:
            self.image = pygame.image.load('ball_colors/ball_green.png').convert_alpha()
        elif randc == 3:
            self.image = pygame.image.load('ball_colors/ball_pink.png').convert_alpha()
        elif randc == 4:
            self.image = pygame.image.load('ball_colors/ball_purple.png').convert_alpha()
        elif randc == 5:
            self.image = pygame.image.load('ball_colors/ball_red.png').convert_alpha()
        elif randc == 6:
            self.image = pygame.image.load('ball_colors/ball_yellow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (2 * r, 2 * r))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(bx, by))

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.check_collision()
        self.check_click()

    def check_collision(self):
        if height - self.r <= self.rect.y + self.r:
            self.vy = -abs(self.vy)
        if self.rect.y + self.r <= self.r:
            self.vy = abs(self.vy)
        if width - self.r <= self.rect.x + self.r:
            self.vx = -abs(self.vx)
        if self.rect.x + self.r <= self.r:
            self.vx = abs(self.vx)

    def check_click(self):
        if (pygame.mouse.get_pos()[0] - self.rect.x - self.r) ** 2 + (
                pygame.mouse.get_pos()[1] - self.rect.y - self.r) ** 2 <= self.r ** 2:
            if pygame.mouse.get_pressed()[0]:
                self.kill()


pygame.init()

width, height = 1500, 800
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

myfont = pygame.font.SysFont("calibri", 30)

n, rmin, rmax, vmax = 0,0,0,0
cat = pygame.image.load('cat.png')

input_box1 = InputBox(width*0.5-150, height*0.25, 40, 40, 'ENTER NUMBER OF BALLS')
input_box2 = InputBox(width*0.5-150, height*0.35, 40, 40, 'ENTER MINIMAL RADIUS (DEFAULT: 20)')
input_box3 = InputBox(width*0.5-150, height*0.45, 40, 40, 'ENTER MAXIMAL RADIUS (DEFAULT: 50)')
input_box4 = InputBox(width*0.5-150, height*0.55, 40, 40, 'ENTER MAXIMUM VELOCITY')

input_boxes = [input_box1, input_box2, input_box3, input_box4]

text1 = myfont.render("BEGIN", 1, (0, 0, 0), (200, 200, 200))
rect1 = text1.get_rect(topleft=(width*0.5, height*0.8))

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

balls = pygame.sprite.Group()
while len(balls) < n:
    randr = random.randint(20, 50)
    randx = random.randint(randr + 1, width - randr - 1)
    randy = random.randint(randr + 1, height - randr - 1)
    randvx = random.randint(-5, 5)
    randvy = random.randint(-5, 5)
    ball = Ball(randr, randx, randy, randvx, randvy)
    balls.add(ball)
    coll = False
    for other in balls:
        if ball != other and pygame.sprite.collide_mask(ball, other):
            coll = True
    if coll:
        ball.kill()

run = True
alldigits = False
context = 'menu'
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if context == 'menu':
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos) and alldigits:
                    n = int(input_box1.text)
                    rmin = int(input_box2.text)
                    rmax = int(input_box3.text)
                    vmax = int(input_box4.text)
                    if rmin == 0 or rmax == 0:
                        rmin = 20
                        rmax = 50
                    if rmin > rmax:
                        t = rmax
                        rmax = rmin
                        rmin = t


                    balls = pygame.sprite.Group()
                    while len(balls) < n:
                        randr = random.randint(rmin, rmax)
                        randx = random.randint(randr + 1, width - randr - 1)
                        randy = random.randint(randr + 1, height - randr - 1)
                        randvx = random.randint(-vmax, vmax)
                        randvy = random.randint(-vmax, vmax)
                        ball = Ball(randr, randx, randy, randvx, randvy)
                        balls.add(ball)
                        coll = False
                        for other in balls:
                            if ball != other and pygame.sprite.collide_mask(ball, other):
                                coll = True
                        if coll:
                            ball.kill()

                    text1 = myfont.render("RESTART", 1, (0, 0, 0), (0, 255, 0))
                    rect1 = text1.get_rect(topleft=(width-150, height-50))
                    context = 'kill'

        elif context =='kill':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    for ball in balls:
                        ball.kill()
                    rect1 = text1.get_rect(topleft=(width/2, height-100))
                    context = 'menu'


    if context == 'menu':
        for box in input_boxes:
            box.update()

        if input_box1.text.isdigit() and input_box2.text.isdigit() and input_box3.text.isdigit() and input_box4.text.isdigit():
            alldigits = True
            text1 = myfont.render("BEGIN", 1, (0, 0, 0), (0, 255, 0))
        else:
            alldigits = False
            text1 = myfont.render("BEGIN", 1, (0, 0, 0), (200, 200, 200))


        window.fill((255, 255, 255))
        for box in input_boxes:
            box.draw(window)
        window.blit(text1, rect1)

    elif context == 'kill':
        collisionbeen = []
        for ball in balls:
            for other in balls:
                if ball != other and pygame.sprite.collide_rect(ball, other) and not (ball, other) in collisionbeen:
                    if pygame.sprite.collide_mask(ball, other):
                        if abs(int(ball.vx)) == 0 and abs(int(ball.vy)) == 0 or abs(int(other.vx)) == 0 and abs(
                                int(other.vy)) == 0:
                            t1, t2 = ball.vx, ball.vy
                            ball.vx, ball.vy = other.vx, other.vy
                            other.vx, other.vy = t1, t2
                        else:
                            lx, ly = (ball.rect.x + ball.r) - (other.rect.x + other.r), (ball.rect.y + ball.r) - (
                                    other.rect.y + other.r)
                            vp1 = (ball.vx ** 2 + ball.vy ** 2) ** 0.5 * (lx * ball.vx + ly * ball.vy) / (
                                    (ball.vx ** 2 + ball.vy ** 2) * (lx ** 2 + ly ** 2)) ** 0.5
                            vp2 = (other.vx ** 2 + other.vy ** 2) ** 0.5 * (lx * other.vx + ly * other.vy) / (
                                    (other.vx ** 2 + other.vy ** 2) * (lx ** 2 + ly ** 2)) ** 0.5
                            dv1, dv2 = vp2 - vp1, vp1 - vp2

                            dv1x = dv1 * lx / (lx ** 2 + ly ** 2) ** 0.5
                            dv1y = dv1 * ly / (lx ** 2 + ly ** 2) ** 0.5

                            dv2x = dv2 * lx / (lx ** 2 + ly ** 2) ** 0.5
                            dv2y = dv2 * ly / (lx ** 2 + ly ** 2) ** 0.5

                            ball.vx += (dv1x)
                            ball.vy += (dv1y)
                            other.vx += (dv2x)
                            other.vy += (dv2y)

                        collisionbeen.append((ball, other))
                        collisionbeen.append((other, ball))
                        # s=0
                        # for bi in balls:
                        #     s += bi.vx**2+bi.vy**2
                        # print(s)

        window.fill((255, 255, 255))
        balls.update()
        balls.draw(window)
        if len(balls) > 0:
            label1 = myfont.render("KILL ALL BALLS IMMEDIATELY (" + str(len(balls)) + " LEFT)", 1, (0, 0, 0))
            label2 = myfont.render("CLICK ON A BALL TO KILL IT", 1, (0, 0, 0))
        else:
            window.blit(cat, (width*0.2, height*0.5-150))
            label1 = myfont.render("WELL DONE", 1, (0, 0, 0))
            label2 = myfont.render("YOU KILLED " + str(n) + " BALLS", 1, (0, 0, 0))
        window.blit(label1, (width*0.2, height*0.2))
        window.blit(label2, (width*0.2, height*0.8))
        window.blit(text1, rect1)

    pygame.display.update()
