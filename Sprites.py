# import random

import pygame.sprite
import os

# from Main import Game

from Settings import *

vec = pygame.math.Vector2

# Assets folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT - 280)
        self.x_speed = 0
        self.y_speed = 0
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 200
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        self.vel.y = -10

    def update(self):
        self.acc = vec(0, 0.3)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.x_speed = 0
        # Wraps around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 600
        # Adds friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos


class Question:
    def __init__(self):

        self.count = 0
        self.signs = ["+", "-", "*", "/"]
        self.signlist = []
        for i in range(300):
            self.signlist.append(random.choice(self.signs))

    # def newQ(self):
        self.addnum1 = random.choice(ADDNUM1)
        self.addnum2 = random.choice(ADDNUM2)
        self.subnum1 = random.choice(SUBNUM1)
        self.subnum2 = random.choice(SUBNUM2)
        self.multnum1 = random.choice(MULTNUM1)
        self.multnum2 = random.choice(MULTNUM2)
        self.divnum1 = random.choice(DIVNUM1)
        self.divnum2 = random.choice(DIVNUM2)

        if self.signlist[self.count] == "+":
            self.question = str(self.addnum1) + " + " + str(self.addnum2)
            self.answer = self.addnum1 + self.addnum2
            self.count += 1

        if self.signlist[self.count] == "-":
            self.question = str(self.subnum1) + " - " + str(self.subnum2)
            self.answer = self.subnum1 - self.subnum2
            self.count += 1

        if self.signlist[self.count] == "*":
            self.question = str(self.multnum1) + " * " + str(self.multnum2)
            self.answer = self.multnum1 * self.multnum2
            self.count += 1

        if self.signlist[self.count] == "/":
            self.question = str(self.divnum1) + " / " + str(self.divnum2)
            self.answer = self.divnum1 / self.divnum2
            self.count += 1


class EntityWrong(pygame.sprite.Sprite, Question):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30))
        # self.image.fill(RED)
        self.wrong_answer = random.choice(ADDNUM1) + random.choice(MULTNUM1)

        # if self.signlist[self.count] == "+":
        #     self.wrong_answer = random.choice(ADDNUM1) + random.choice(ADDNUM2)
        #
        # if Qsign == "-":
        #     self.wrong_answer = random.choice(SUBNUM1) - random.choice(SUBNUM2)
        #
        # if Qsign == "*":
        #     self.wrong_answer = random.choice(MULTNUM1) * random.choice(MULTNUM2)
        #
        # if Qsign == "/":
        #     self.wrong_answer = random.choice(DIVNUM1) / random.choice(DIVNUM2)

        self.font_name = pygame.font.match_font(FONT)
        self.my_font = pygame.font.SysFont(FONT, 30)
        self.image = self.my_font.render(str(self.wrong_answer), False, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-450, -10)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        # self.rect.x = self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-250, -10)
            self.speedy = random.randrange(1, 4)


class EntityCorrect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30))
        # self.image.fill(GREEN)

        self.zero = 0
        self.font_name = pygame.font.match_font(FONT)
        self.my_font = pygame.font.SysFont(FONT, 30)
        self.image = self.my_font.render(str(self.zero), False, RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -10)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        # self.rect.x = self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-250, -10)
            self.speedy = random.randrange(1, 4)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        # self.image = pygame.image.load(os.path.join(img_folder, "Platform.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y