from GameLogic.classes.generic import Base
import math


class Ball(Base):
    def __init__(self, height: float, width: float):
        x1 = width * 0.4 - 5
        x2 = width * 0.4 + 5
        y1 = height - 10
        y2 = height - 20

        super().__init__(x1, y1, x2, y2, height=height, width=width)
        self._speed = 15
        self._direction = 3* math.pi/4
        self.renderer = None

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, pDirection):
        delta = math.pi/30
        if (math.pi/2) - delta > pDirection > (math.pi/2) + delta:
            self._direction = math.pi/2 + delta
        elif -delta > pDirection > delta:
            self._direction = delta * abs(delta)/delta
        elif math.pi - delta > pDirection > math.pi + delta:
            self._direction = math.pi + delta * abs(delta) / delta
        elif 3*(math.pi/2) - delta > pDirection > 3*(math.pi/2) + delta:
            self._direction = 3*(math.pi/2) + delta
        else:
            self._direction = pDirection

    def increase_speed(self, increment: float):
        self._speed += increment

    def render_ball(self, canvas):
        self.renderer = canvas.create_oval(self._x1, self._y1, self._x2, self._y2, fill='#4A4A4A')

    def update_cords(self, coords):
        self._x1 = coords[0]
        self._x2 = coords[2]
        self._y1 = coords[1]
        self._y2 = coords[3]

    def move_candidate(self, step):
        return {
            'x1': self._x1 + step * math.cos(self._direction),
            'y1': self._y1 - step * math.sin(self._direction),
            'x2': self._x2 + step * math.cos(self._direction),
            'y2': self._y2 - step * math.sin(self._direction)
        }

    @staticmethod
    def collides(obj_coords: dict, obstacle: dict, vertical=None):
        if vertical is None:
            return (
                (obj_coords['y1'] >= obstacle['y2'] and obj_coords['y2'] <= obstacle['y1'] and obj_coords['x2']>=obstacle['x1'] and obj_coords['x1']<= obstacle['x2']) or
                (obj_coords['y2'] <= obstacle['y1'] and obj_coords['y1'] >= obstacle['y2'] and obj_coords['x2']>=obstacle['x1'] and obj_coords['x1']<= obstacle['x2']) or
                (obj_coords['x1'] <= obstacle['x2'] and obj_coords['x2'] >= obstacle['x1'] and obj_coords['y2']>=obstacle['y1'] and obj_coords['y1']<= obstacle['y2']) or
                (obj_coords['x2'] >= obstacle['x1'] and obj_coords['x1'] <= obstacle['x2'] and obj_coords['y2']>=obstacle['y1'] and obj_coords['y1']<= obstacle['y2'])
            )

        elif vertical:
            return not (obj_coords['y1'] > obstacle['y2'] or obj_coords['y1'] >obstacle['y2'])
        else:
            return not (obj_coords['x1'] > obstacle['x2'] or obj_coords['x2'] < obstacle['x1'])

    @staticmethod
    def angle_movement(theta, factor):
        return 0.8*theta + 0.2*\
               (math.atan(factor*10 - 5))

    def check_borders(self, canvas):
        # LEFT BORDER
        if self._x1 + self._speed * math.cos(self.direction) < 0:
            r_ = abs(self._x1 / math.cos(self.direction))

            canvas.move(self.renderer, r_ * math.cos(self.direction),
                        -r_ * math.sin(self.direction))

            self.update_cords(canvas.coords(self.renderer))
            self.direction = math.pi - self.direction

        #RIGHT BORDER
        elif self._x2 + self._speed * math.cos(self.direction) > self.width * 0.8:
            r_ = abs((self.width * 0.8 - self._x2) / math.cos(self.direction))

            canvas.move(self.renderer, r_ * math.cos(self.direction),
                        -r_ * math.sin(self.direction))

            self.update_cords(canvas.coords(self.renderer))
            self.direction = math.pi - self.direction

        #TOP BORDER
        elif self._y1 - self._speed * math.sin(self.direction) < 0:

            r_ = abs(self._y1 / math.sin(self.direction))

            canvas.move(self.renderer, r_ * math.cos(self.direction),
                        -r_ * math.sin(self.direction))

            self.update_cords(canvas.coords(self.renderer))

            self.direction = - self.direction

        #BOTTOM BORDER (LOSING LOGIC)
        elif self._y2 - self._speed * math.sin(self.direction) >= self.height:
            paddle_coords = canvas.paddle.get_coords()
            if self._x1 >= paddle_coords[0] and self._x2 <= paddle_coords[2]:
                r_ = abs((self.height - self._y2 - 4) / math.sin(self.direction))

                canvas.move(self.renderer, r_ * math.cos(self.direction),
                            -r_ * math.sin(self.direction))

                self.update_cords(canvas.coords(self.renderer))
                ball_center = self.get_center('x')
                paddle_center = canvas.paddle.get_center('x')

                angle_X = ball_center - paddle_center
                angle_Origin = (- self.direction)
                angle_computed = math.radians(-70/(canvas.paddle.get_width()/2)*angle_X + 90)

                self.direction = (1 - (abs(angle_X) / (canvas.paddle.get_width() / 2)) ** 0.25) * angle_Origin + ((abs(angle_X) / (canvas.paddle.get_width() / 2)) ** 0.25) * angle_computed
                # self.direction = angle_Origin
            else:
                canvas.status = 1

        #FREE MOVEMENT (NO BORDERS)
        else:
            canvas.move(self.renderer, self._speed * math.cos(self.direction),
                        -self._speed * math.sin(self.direction))
            self.update_cords(canvas.coords(self.renderer))

    def move(self, canvas):
        self.update_cords(canvas.coords(self.renderer))
        next_move = self.move_candidate(self._speed)
        collision_brick_list = []
        collision_brick_coords_list = []
        if self.collides(next_move, canvas.bricks.limits):
            #Con quien me choco?
            for step in range(1, self._speed+1):
                if not collision_brick_list:
                    for key, brick in canvas.bricks.brick_dict.items():

                        brick_coords = brick.get_coord_dict()
                        # print(self.collides(self.move_candidate(step), brick_coords))
                        if self.collides(self.move_candidate(step), brick_coords):
                            collision_brick_list.append(brick)
                            collision_brick_coords_list.append(brick_coords)

            if not collision_brick_list:
                self.check_borders(canvas)
            else:
                for idx, collision_brick in enumerate(collision_brick_list):
                    collision_brick_coords = collision_brick_coords_list[idx]
                    ls = []
                    profiles = [
                        ['x1', collision_brick_coords['x1'], collision_brick_coords['y1'], collision_brick_coords['y2'], 'x2'],
                        ['x2', collision_brick_coords['x2'], collision_brick_coords['y1'], collision_brick_coords['y2'], 'x1'],
                        ['y1', collision_brick_coords['y1'], collision_brick_coords['x1'], collision_brick_coords['x2'], 'y2'],
                        ['y2', collision_brick_coords['y2'], collision_brick_coords['x1'], collision_brick_coords['x2'], 'y1']
                    ]

                ball_coords = self.get_coord_dict()

                for idx, ar in enumerate(profiles):
                    if idx <= 1:
                        l = (ar[1] - ball_coords[ar[4]])/math.cos(self._direction)
                        adjustment = -5 if ar[0][1] == '2' else 5
                        if (ar[2] <= ball_coords['y1'] - l*math.sin(self._direction) <= ar[3] or ar[2] <= ball_coords['y2'] - l*math.sin(self._direction) <= ar[3]) and l > 0:
                            ls.append(l)
                        else:
                            ls.append(1e9)
                    else:
                        l = -(ar[1] - ball_coords[ar[4]])/math.sin(self._direction)
                        if (ar[2] <= ball_coords['x1'] + l*math.cos(self._direction) <= ar[3] or ar[2] <= ball_coords['x2'] + l*math.cos(self._direction) <= ar[3]) and l > 0:
                            ls.append(l)
                        else:
                            ls.append(1e9)


                profile = ls.index(min(ls)) % 4
                brick = collision_brick_list[ls.index(min(ls)) // 4]
                l = min(ls)

                if l == 1e9:
                    self.check_borders(canvas)
                else:
                    canvas.move(self.renderer, l*math.cos(self._direction), -l*math.sin(self._direction))
                    self.update_cords(canvas.coords(self.renderer))


                    canvas.remove_brick(brick)

                    if profiles[profile][0][0] == 'x':
                        self.direction = math.pi - self.direction
                    else:
                        self.direction = -self.direction
        else:
            self.check_borders(canvas)
