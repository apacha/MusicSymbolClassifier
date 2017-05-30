from sympy import Point2D


class Rectangle:
    def __init__(self, origin: Point2D, width: int, height: int) -> None:
        super().__init__()
        self.height = height
        self.width = width
        self.origin = origin

    def __eq__(self, o: object) -> bool:
        are_equal = self.width == o.width and self.height == o.height and self.origin == o.origin
        return are_equal
