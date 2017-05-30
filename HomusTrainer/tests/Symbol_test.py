import os
import unittest

from sympy import Point2D

from datasets.Rectangle import Rectangle
from datasets.Symbol import Symbol


class Symbol_test(unittest.TestCase):
    def test_initialize_from_empty_string_expect_empty_symbol(self):
        # Arrange

        # Act
        symbol = Symbol.initialize_from_string("")

        # Assert
        self.assertIsNone(symbol)

    def test_initialize_with_simple_symbol(self):
        # Arrange
        content = "test\n23,107;30,101;"
        strokes = [[Point2D(23, 107), Point2D(30, 101)]]
        dimensions = Rectangle(Point2D(23, 101), 8, 7)

        # Act
        symbol = Symbol.initialize_from_string(content)

        # Assert
        self.assertIsNotNone(symbol)
        self.assertEqual("test", symbol.symbol_name)
        self.assertEqual(content, symbol.content)
        self.assertEqual(strokes, symbol.strokes)
        self.assertEqual(dimensions, symbol.dimensions)

    def test_initialize_with_real_symbol(self):
        content = "12-8-Time\n28,107;30,107;30,110;25,121;19,131;13,139;10,144;9,145;10,145;10,145;\n35,115;35,115;37,115;39,115;42,116;43,117;42,120;39,124;33,131;30,134;29,137;32,138;36,139;41,140;42,140;42,141;42,141;\n26,159;27,159;30,158;36,158;38,159;38,160;35,163;31,166;24,172;21,176;20,180;21,182;23,182;26,178;26,175;25,171;24,166;23,159;20,158;20,158;"

        # Act
        symbol = Symbol.initialize_from_string(content)

        # Assert
        self.assertIsNotNone(symbol)
        self.assertEqual("12-8-Time", symbol.symbol_name)
        self.assertEqual(content, symbol.content)
        self.assertEqual(3, len(symbol.strokes), "We expected three strokes")

    def test_draw_into_bitmap(self):
        # Arrange
        symbol = Symbol("", [[Point2D(0, 0), Point2D(100, 100)]], "", Rectangle(Point2D(0, 0), 100, 100))
        export_path = "test_bitmap.png"

        # Act
        symbol.draw_into_bitmap(export_path, 2, 2, 102, 102)

        # Assert
        self.assertTrue(os.path.exists(export_path))

        # Cleanup
        os.remove(export_path)


if __name__ == '__main__':
    unittest.main()
