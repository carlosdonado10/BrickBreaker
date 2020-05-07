from GameLogic.classes.generic import Base


class Paddle(Base):
    def __init__(self, height: float, width: float):
        x1 = int(width * 0.4 - 50)
        y1 = height
        x2 = int(width * 0.4 + 50)
        y2 = height - 4
        super().__init__(x1, y1, x2, y2, height=height, width=width)
        self.renderer = None

    def render_paddle(self, canvas):
        self.renderer = canvas.create_rectangle(self._x1, self._y1, self._x2, self._y2, fill='#000000')

    def update_cords(self, dx):
        self._x1 += dx
        self._x2 += dx

    def move(self, canvas):

        movement = 50 if canvas.move_right and self._x2 < self.width*0.8 else -30 \
                        if canvas.move_left and self._x1 > 0 else 0


        if movement != 0:
            canvas.move(self.renderer, movement, 0)
            self.update_cords(movement)
