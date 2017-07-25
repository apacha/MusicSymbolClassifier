import unittest

from hamcrest import *
from sympy import Point2D

from datasets.Rectangle import Rectangle


class Rectangle_test(unittest.TestCase):
    def test_rectangles_that_overlap(self):
        # Arrange
        r1 = Rectangle(Point2D(1, 1), 2, 2)
        r2 = Rectangle(Point2D(2, 2), 2, 2)

        # Act & Assert
        self.assertTrue(Rectangle.overlap(r1, r2))
        self.assertTrue(Rectangle.overlap(r2, r1))

    def test_rectangles_that_do_not_overlap(self):
        # Arrange
        r1 = Rectangle(Point2D(1, 1), 2, 2)
        r2 = Rectangle(Point2D(2, 2), 2, 2)
        r3 = Rectangle(Point2D(3, 6), 9, 5)
        r4 = Rectangle(Point2D(7, 7), 4, 3)

        # Act & Assert
        self.assertFalse(Rectangle.overlap(r1, r3))
        self.assertFalse(Rectangle.overlap(r1, r4))
        self.assertFalse(Rectangle.overlap(r2, r3))
        self.assertFalse(Rectangle.overlap(r2, r4))
        self.assertFalse(Rectangle.overlap(r3, r1))
        self.assertFalse(Rectangle.overlap(r3, r2))
        self.assertFalse(Rectangle.overlap(r4, r1))
        self.assertFalse(Rectangle.overlap(r4, r2))

    def test_rectangles_that_are_enclosed(self):
        # Arrange
        r3 = Rectangle(Point2D(3, 6), 9, 5)
        r4 = Rectangle(Point2D(7, 7), 4, 3)

        # Act & Assert
        self.assertTrue(Rectangle.overlap(r3, r4))
        self.assertTrue(Rectangle.overlap(r4, r3))

    def test_rectangles_that_cross_without_corner_overlap(self):
        # Arrange
        r5 = Rectangle(Point2D(13, 11), 6, 2)
        r6 = Rectangle(Point2D(13, 9), 2, 5)

        # Act & Assert
        self.assertTrue(Rectangle.overlap(r5, r6))
        self.assertTrue(Rectangle.overlap(r6, r5))

    def test_merge_rectangles_that_overlap(self):
        # Arrange
        r7 = Rectangle(Point2D(1, 1), 2, 2)
        r8 = Rectangle(Point2D(2, 1), 1, 4)
        expected = Rectangle(Point2D(1, 1), 2, 4)

        # Act
        merge = Rectangle.merge(r7, r8)

        # Assert
        assert_that(merge, equal_to(expected))

    def test_merge_rectangles_that_do_not_overlap(self):
        # Arrange
        r7 = Rectangle(Point2D(1, 1), 2, 2)
        r9 = Rectangle(Point2D(5, 3), 1, 1)
        expected = Rectangle(Point2D(1, 1), 5, 3)

        # Act
        merge = Rectangle.merge(r7, r9)

        # Assert
        assert_that(merge, equal_to(expected))

if __name__ == '__main__':
    unittest.main()
