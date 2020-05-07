class Base:
    def __init__(self, x1: float, y1: float, x2: float, y2: float, height: float, width: float):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self.height = height
        self.width = width
        self.colors = {
            "r": "#e74c3c",
            "g": "#2ecc71",
            "b": "#3498db",
            "t": "#1abc9c",
            "p": "#9b59b6",
            "y": "#f1c40f",
            "o": "#e67e22",
        }

    def get_color(self, col: str):
        col = self.colors.get(col)
        if col:
            return col
        else:
            raise ValueError(f'{col} is not recognizes as an internal color')

    def get_coords(self):
        return tuple((self._x1, self._y1, self._x2, self._y2))

    def get_coord_dict(self):
        return {'x1': self._x1, 'y1': self._y1, 'x2': self._x2, 'y2': self._y2}

    def get_center(self, axis:str):
        if axis not in ['x', 'y']:
            raise ValueError('axis is not x or y')

        if axis =='x':
            return self._x2 - (self._x2 - self._x1)/2

        else:
            return self._y2 - (self._y2 - self._y1) / 2

    def get_width(self):
        return self._x2 - self._x1

