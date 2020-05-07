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

        self.move_left, self.move_right = False, False
        if self.status == 0:
            self.after(int(1000/60), self.evolve)

          # TODO:Ancho de la barra en variable


def move_right(event):
    global brick_breaker
    print('moved right')
    brick_breaker.move_right = True


def move_left(event):
    global brick_breaker
    print('moved left')
    brick_breaker.move_left = True


if __name__ == '__main__':
    m = tk.Tk()
    m.bind("<Left>", move_left)
    m.bind("<Right>", move_right)
    # canvas=tk.Canvas(master=m, height=100, width=100)
    # canvas.create_oval(90, 90, 110, 110, width=0, fill="ivory3")
    brick_breaker = Canvas(m)
    tk.mainloop()
