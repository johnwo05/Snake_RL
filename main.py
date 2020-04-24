import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
import numpy as np
import math

vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font('FONT_NAME')
        self.HIGHSCORE = 0
        self.SCORE = 0
        self.GENERATION = 1

        self.game_time = 0

        self.TRAINING = False


        self.GAMMA = 0.8


        self.dir = path.dirname(__file__)
        self.Q = path.join(self.dir,Q_FILE)
        self.saved_Q = path.join(self.dir,saved_Q)
        self.load_data()



    def load_data(self):
        # load high SCORE

        with open(path.join(self.dir,SCORE_FILE), 'r+') as f:
            try:
                self.HIGHSCORE = int(f.read())
            except:
                self.SCORE = 0

        with open(path.join(self.dir,GENERATION_FILE), 'r+') as f:
            try:
                self.GENERATION = int(f.read())
            except:
                self.GENERATION = 0


        if self.TRAINING:

            self.Q_MATRIX = np.loadtxt(self.Q)

        else:
            self.Q_MATRIX = np.loadtxt(self.saved_Q)





    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.body = pg.sprite.Group()


        self.vision_field =  np.array([[7,8,9,10,11,12,13,7,8,9,10,11,12,13,7,8,9,10,11,12,13,7,8,9,11,12,13,7,8,9,10,11,12,13,7,8,9,10,11,12,13,7,8,9,10,11,12,13],[7,7,7,7,7,7,7,8,8,8,8,8,8,8,9,9,9,9,9,9,9,10,10,10,10,10,10,11,11,11,11,11,11,11,12,12,12,12,12,12,12,13,13,13,13,13,13,13]])

        self.player = Player(self, 10, 10)



        self.food = Food(self)

        for x in range(0, 32):
            Wall(self, x, 0)
        for x in range(0, 32):
            Wall(self, x , 23)

        for y in range(0, 23):
            Wall(self, 0, y)

        for y in range(0, 23):
            Wall(self, 31, y)
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.running = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.game_time += self.dt
            # print(self.game_time)

            self.events()
            np.savetxt(self.saved_Q,self.Q_MATRIX)
            self.update()
            self.draw()
        self.SCORE = 0

    def quit(self):
        if self.TRAINING:
            np.savetxt(self.Q,self.Q_MATRIX)
            np.savetxt(self.saved_Q,self.Q_MATRIX)

            self.GENERATION +=1

            with open(path.join(self.dir,GENERATION_FILE), 'w') as f:
                f.write(str(self.GENERATION))
        else:
            np.savetxt(self.saved_Q,self.Q_MATRIX)


        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        if self.player.hit_wall:
            self.playing = False
            if self.SCORE > self.HIGHSCORE:
                self.HIGHSCORE = self.SCORE
                with open(path.join(self.dir,SCORE_FILE), 'w') as f:
                    f.write(str(self.SCORE))
                    self.SCORE = 0

        if self.game_time > 600:
            self.playing = False



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(str('Score: ') , 40, WHITE, 2 * TILESIZE, 24 * TILESIZE)
        self.draw_text(str(self.SCORE) , 40, WHITE, 4 * TILESIZE, 24 * TILESIZE)

        self.draw_text(str('Generation:       ') , 40, WHITE, 24 * TILESIZE, 24 * TILESIZE)
        self.draw_text(str(self.GENERATION) , 40, WHITE, 27 * TILESIZE, 24 * TILESIZE)

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                if event.key == pg.K_LEFT:
                    if self.player.dx != -1 and self.player.dx != 1:
                        self.player.move(dx=-1)

                if event.key == pg.K_RIGHT:
                    if self.player.dx != -1 and self.player.dx !=1:
                        self.player.move(dx=1)



                if event.key == pg.K_UP:
                    if self.player.dy != -1 and self.player.dy !=1:
                        self.player.move(dy=-1)

                if event.key == pg.K_DOWN:
                    if self.player.dy != -1 and self.player.dy !=1:
                        self.player.move(dy=1)







        #self.player.move_body()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(LIGHTGREY)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any Key to start the A.I.", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        # self.draw_text("In main.py, Set TRAINING to tru", 22,  WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("A.I. HIGH SCORE: " + str(self.HIGHSCORE), 22, WHITE,  WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # waiting = False
                    # self.running = False


                    #Write Q to file if Quitting



                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_go_screen(self):
        # game over/continue

        #Change This if you want to modify Game Over Screen. Click X to view screen
        if not self.running:
            return

        self.screen.fill(LIGHTGREY)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22,  WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.SCORE > self.HIGHSCORE:
            self.HIGHSCORE = self.SCORE
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir,SCORE_FILE), 'w') as f:
                f.write(str(self.SCORE))
        else:
            self.draw_text("High Score: " + str(self.HIGHSCORE), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)


        pg.display.flip()
        self.wait_for_key()
        self.SCORE = 0
        pass



# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()

    if g.TRAINING:

        np.savetxt(g.Q,g.Q_MATRIX)
        g.GENERATION +=1

        with open(path.join(g.dir,GENERATION_FILE), 'w') as f:
            f.write(str(g.GENERATION))



    if not g.TRAINING:
        if g.TRAINING:

            np.savetxt(g.Q,g.Q_MATRIX)
            g.GENERATION +=1

            with open(path.join(g.dir,GENERATION_FILE), 'w') as f:
                f.write(str(g.GENERATION))
