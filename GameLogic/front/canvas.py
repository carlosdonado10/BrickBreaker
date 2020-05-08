import tkinter as tk
from GameLogic.classes.paddle import Paddle
from GameLogic.classes.ball import Ball
from GameLogic.classes.brick import ActiveBricks
import time

class Canvas(tk.Canvas):

    def __init__(self, root):
        self.SCREENHEIGHT = 500
        self.BRICKSBYLINE = 16
        self.SCREENWIDTH = 800

        tk.Canvas.__init__(self, master=root, width=self.SCREENWIDTH, height=self.SCREENHEIGHT)
        self.pack()
        self.create_game_area()

        self.paddle = Paddle(height=self.SCREENHEIGHT, width=self.SCREENWIDTH)
        self.paddle.render_paddle(self)

        self.ball = Ball(self.SCREENHEIGHT, self.SCREENWIDTH)
        self.ball.render_ball(self)

        self.bricks = ActiveBricks(level=1, canvas=self)

        self.status = 0  #0: playing, 1: lost, 2: won


        self._level = 1
        self.move_right = False
        self.move_left = False
        self.MAX_LEVELS = 10

        self.evolve()

    def pass_level(self):
        if self.level < self.MAX_LEVELS:
            self._level += 1
        else:
            raise ValueError('Game Finished!')

    def create_game_area(self):
        self.create_rectangle(0, 0, self.SCREENWIDTH * 0.8, self.SCREENHEIGHT, fill='#9DA197')

    def remove_brick(self, brick):
        self.bricks.remove_brick(id(brick))
        self.delete(brick.renderer)

    def evolve(self):
        time.sleep(1/60)
        self.ball.move(self)
        self.paddle.move(self)
        if self.bricks.brick_dict == {}:
            self.status = 2

        self.move_left, self.move_right = False, False
        if self.status == 0:
            self.after(int(1000/60), self.evolve)

          # TODO:Ancho de la barra en variable


