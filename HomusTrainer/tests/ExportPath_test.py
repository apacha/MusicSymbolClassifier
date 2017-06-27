import os
import unittest

from sympy import Point2D

from datasets.ExportPath import ExportPath
from datasets.Rectangle import Rectangle
from datasets.Symbol import Symbol


class ExportPath_test(unittest.TestCase):
    def test_initialize_from_empty_string_expect_empty_symbol(self):
        # Arrange
        export_path = ExportPath("data/images","3-4-Time", "1-13", 3, "png")

        # Act
        full_path = export_path.get_full_path()

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("data/images/3-4-Time/1-13_3.png", full_path)

    def test_initialize_with_simple_symbol(self):
        # Arrange
        export_path = ExportPath("data/images","3-4-Time", "1-13", 3, "png")

        # Act
        full_path = export_path.get_full_path(33)

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("data/images/3-4-Time/1-13_3_offset_33.png", full_path)

if __name__ == '__main__':
    unittest.main()
