import tkinter as tk
from GameLogic.front.canvas import Canvas

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
    brick_breaker = Canvas(m)
    tk.mainloop()
