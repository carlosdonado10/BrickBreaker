from GameLogic.classes.generic import Base
from utils.reader import Reader


class Brick(Base):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color: str, resistance: int):
        super().__init__(x1, y1, x2, y2, 0, 0)
        self._color = self.get_color(color)
        self._resistance = resistance
        self.lives = resistance
        self.renderer = None

    def get_id(self):
        return id(self)

    def is_hit(self):
        self._resistance -= 1

    def render_brick(self, canvas):
        self.renderer = canvas.create_rectangle(self._x1, self._y1, self._x2, self._y2, fill=self._color)


class ActiveBricks:

    def __init__(self, level, canvas):
        self.brick_dict = self.render_level(level, canvas)
        self.limits = self.update_limits({}, self.brick_dict, brick=None, initial=True)

    @staticmethod
    def render_level(level, canvas):
        data = Reader.read_level(level)
        brick_dict = {}
        y1, y2 = 30, 60
        for idx, rw in enumerate(data):
            x1, x2 = 0, int(canvas.SCREENWIDTH*0.8/10)
            for brk in rw[1:]:
                if brk:
                    brick = Brick(x1, y1, x2, y2, color=brk, resistance=rw[0])
                    brick.render_brick(canvas)
                    brick_dict[id(brick)] = brick
                else:
                    pass

                x1 += int(canvas.SCREENWIDTH*0.8/10)
                x2 += int(canvas.SCREENWIDTH*0.8/10)

            y1 +=30
            y2 +=30
        return brick_dict

    @staticmethod
    def update_limits(limits, bricks_dict, brick=None, initial=False):
        if not initial and brick is None:
            raise ValueError('No brick was provided')

        if not initial and limits == {}:
            raise ValueError('Run the initiation first')

        if initial:
            limits.update({
                'x1': min(bricks_dict.items(), key=lambda x:x[1]._x1)[1]._x1,
                'x2': max(bricks_dict.items(), key=lambda x:x[1]._x2)[1]._x2,
                'y1': min(bricks_dict.items(), key=lambda x:x[1]._y1)[1]._y1,
                'y2': max(bricks_dict.items(), key=lambda x:x[1]._y2)[1]._y2,
            })

            return limits
        else:
            raise ValueError('Functionality not added (Update given a collided bick (if necessary)')

    def remove_brick(self, key):
        del self.brick_dict[key]
