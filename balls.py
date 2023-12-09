import random

import pygame


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
        if (pygame.mouse.get_pos()[0]-self.rect.x-self.r)**2+(pygame.mouse.get_pos()[1]-self.rect.y-self.r)**2 <= self.r**2:
            if pygame.mouse.get_pressed()[0]:
                self.kill()


pygame.init()

width, height = 800, 800
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

balls = pygame.sprite.Group()
while len(balls) < 10:
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
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    collisionbeen = []
    for ball in balls:
        for other in balls:
            if ball != other and pygame.sprite.collide_rect(ball, other) and not (ball, other) in collisionbeen:
                if pygame.sprite.collide_mask(ball, other):
                    if abs(int(ball.vx)) == 0 and abs(int(ball.vy)) == 0 or abs(int(other.vx)) == 0 and abs(int(other.vy)) == 0:
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
                    s=0
                    for bi in balls:
                        s += bi.vx**2+bi.vy**2
                    print(s)

    window.fill((255, 255, 255))
    balls.update()
    balls.draw(window)

    pygame.display.update()
