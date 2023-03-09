import pygame
from Sprites import *
from Settings import *
vec = pygame.math.Vector2


# Assets folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


# Template for the player
class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # initialize game window
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brain Drain")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)
        # self.sign = random.choice(SIGN)
        self.main_wrong_answer = 0
        # self.question = 0
        # self.answer = 0
        self.score = 0

        # self.count = 0
        # self.signs = ["+", "-", "*", "/"]
        # self.signlist = []
        # for i in range(300):
        #     self.signlist.append(random.choice(self.signs))

    def newquestion(self):
        # Creates a new question
        self.q = Question()
        # self.q.newQ()
        self.question = self.q.question
        self.answer = self.q.answer

        print(self.question)
        print(self.answer)

        # self.addnum1 = random.choice(ADDNUM1)
        # self.addnum2 = random.choice(ADDNUM2)
        # self.subnum1 = random.choice(SUBNUM1)
        # self.subnum2 = random.choice(SUBNUM2)
        # self.multnum1 = random.choice(MULTNUM1)
        # self.multnum2 = random.choice(MULTNUM2)
        # self.divnum1 = random.choice(DIVNUM1)
        # self.divnum2 = random.choice(DIVNUM2)
        #
        # if self.signlist[self.count] == "+":
        #     self.question = str(self.addnum1) + " + " + str(self.addnum2)
        #     self.answer = self.addnum1 + self.addnum2
        #     self.count += 1
        #
        # if self.signlist[self.count] == "-":
        #     self.question = str(self.subnum1) + " - " + str(self.subnum2)
        #     self.answer = self.subnum1 - self.subnum2
        #     self.count += 1
        #
        # if self.signlist[self.count] == "*":
        #     self.question = str(self.multnum1) + " * " + str(self.multnum2)
        #     self.answer = self.multnum1 * self.multnum2
        #     self.count += 1
        #
        # if self.signlist[self.count] == "/":
        #     self.question = str(self.divnum1) + " / " + str(self.divnum2)
        #     self.answer = self.divnum1 / self.divnum2
        #     self.count += 1

    def new(self):
        # Starts a new game

        self.score = 0
        self.newquestion()
        self.bg = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg_rect = self.bg.get_rect()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.wrong_entities = pygame.sprite.Group()
        self.right_entities = pygame.sprite.Group()

        for i in range(12):
            ew = EntityWrong()
            self.all_sprites.add(ew)
            self.wrong_entities.add(ew)

        ec = EntityCorrect()
        self.all_sprites.add(ec)
        self.right_entities.add(ec)

        self.player = Player()
        self.all_sprites.add(self.player)
        p1 = Platform(65, HEIGHT - 250, WIDTH - 160, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:

            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Updates game loop
        self.all_sprites.update()

        wrong_hits = pygame.sprite.spritecollide(self.player, self.wrong_entities, False)
        if wrong_hits:
            for sprites in self.all_sprites:
                sprites.kill()
                self.playing = False

        right_hits = pygame.sprite.spritecollide(self.player, self.right_entities, False)
        if right_hits:
            for sprites in self.right_entities:
                sprites.kill()
            self.score += 1

            self.newquestion()

            ec = EntityCorrect()
            self.all_sprites.add(ec)
            self.right_entities.add(ec)

        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 5

        if self.player.rect.bottom > HEIGHT + 50:
            for sprites in self.all_sprites:
                sprites.kill()
                self.playing = False

    def events(self):
        # Game loop events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Draws elements
        self.screen.fill(DBLUE)
        self.screen.blit(self.bg, self.bg_rect)
        # self.screen.blit(self.text_surface, (WIDTH / 2, 200))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.question), 50, WHITE, WIDTH / 2, 15)
        self.draw_text(str(self.score), 100, WHITE, WIDTH / 2, 700)
        # after drawing everything, flip the display
        pygame.display.flip()

    def draw_text(self, text, size, colour, x, y):
        # Draws text on screen
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
while g.running:
    g.new()

# Quit if running is false
pygame.quit()
