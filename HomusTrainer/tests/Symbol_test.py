import os
import unittest

from sympy import Point2D

from datasets.ExportPath import ExportPath
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
        self.assertEqual("test", symbol.symbol_class)
        self.assertEqual(content, symbol.content)
        self.assertEqual(strokes, symbol.strokes)
        self.assertEqual(dimensions, symbol.dimensions)

    def test_initialize_with_real_symbol(self):
        content = "12-8-Time\n28,107;30,107;30,110;25,121;19,131;13,139;10,144;9,145;10,145;10,145;\n35,115;35," \
                  "115;37,115;39,115;42,116;43,117;42,120;39,124;33,131;30,134;29,137;32,138;36,139;41,140;42,140;42," \
                  "141;42,141;\n26,159;27,159;30,158;36,158;38,159;38,160;35,163;31,166;24,172;21,176;20,180;21," \
                  "182;23,182;26,178;26,175;25,171;24,166;23,159;20,158;20,158;"

        # Act
        symbol = Symbol.initialize_from_string(content)

        # Assert
        self.assertIsNotNone(symbol)
        self.assertEqual("12-8-Time", symbol.symbol_class)
        self.assertEqual(content, symbol.content)
        self.assertEqual(3, len(symbol.strokes), "We expected three strokes")

    def test_draw_into_bitmap(self):
        # Arrange
        symbol = Symbol("", [[Point2D(0, 0), Point2D(100, 100)]], "", Rectangle(Point2D(0, 0), 100, 100))
        export_path = ExportPath("","","bitmap",2)

        # Act
        symbol.draw_into_bitmap(export_path, 2, 2, 102, 102)

        # Assert
        self.assertTrue(os.path.exists(export_path.get_full_path()))

        # Cleanup
        os.remove(export_path.get_full_path())

    def test_draw_staff_lines(self):
        content = "Quarter-Note\n144,130;144,130;143,130;141,130;139,130;138,131;138,131;138,133;140,135;143,135;146," \
                  "135;150,132;154,128;155,126;153,124;150,124;146,124;142,125;140,127;140,128;141,129;144,130;149," \
                  "129;152,128;153,126;153,124;150,123;147,122;144,123;142,125;140,126;141,128;143,128;146,127;149," \
                  "126;151,124;151,122;148,121;145,122;141,125;138,129;137,131;138,132;141,132;144,131;147,128;148," \
                  "126;148,125;147,125;145,126;144,127;144,129;144,129;147,130;149,130;150,129;150,128;150,127;148," \
                  "127;147,128;147,129;147,130;148,131;151,131;153,130;153,129;154,127;152,126;150,126;148,126;147," \
                  "127;147,128;147,129;148,130;148,130;148,130;146,130;144,130;141,131;140,131;139,131;139,131;139," \
                  "131;139,131;139,131;140,131;140,133;141,137;141,143;141,150;141,158;139,172;139,180;139,188;140," \
                  "192;141,195;142,196;143,196;144,196;144,196;144,197;144,197;"
        export_path = ExportPath("","","test",3)
        symbol = Symbol.initialize_from_string(content)

        # Act
        offsets = [18 + 7 * i for i in range(20)]  # [18,25,32,39,46,53,60,67,74,81,88]
        bounding_boxes = dict()
        symbol.draw_into_bitmap(export_path, 3, 0, 128, 224, 14, offsets, bounding_boxes)

        # Assert
        bounding_box_in_image = bounding_boxes["test_3_offset_144.png"]
        self.assertEqual(bounding_box_in_image.origin, Point2D(109/2,147/2))
        self.assertEqual(bounding_box_in_image.width, 19)
        self.assertEqual(bounding_box_in_image.height, 77)

if __name__ == '__main__':
    unittest.main()
