import os
from typing import List

import sys

from PIL import ImageDraw
from sympy import Point2D
from PIL import Image
from datasets.Rectangle import Rectangle


class Symbol:
    def __init__(self, content: str, strokes: List[List[Point2D]], symbol_name: str, dimensions: Rectangle) -> None:
        super().__init__()
        self.dimensions = dimensions
        self.symbol_name = symbol_name
        self.content = content
        self.strokes = strokes

    @staticmethod
    def initialize_from_string(content: str) -> 'Symbol':
        """
        Create and initializes a new symbol from a string
        :param content: The content of a symbol as read from the text-file
        :return: The initialized symbol
        :rtype: Symbol
        """

        if content is None or content is "":
            return None

        lines = content.splitlines()
        min_x = sys.maxsize
        max_x = 0
        min_y = sys.maxsize
        max_y = 0

        symbol_name = lines[0]
        strokes = []

        for stroke_string in lines[1:]:
            stroke = []

            for point_string in stroke_string.split(";"):
                if point_string is "":
                    continue  # Skip the last element, that is due to a trailing ; in each line

                point_x, point_y = point_string.split(",")
                x = int(point_x)
                y = int(point_y)
                stroke.append(Point2D(x, y))

                max_x = max(max_x, x)
                min_x = min(min_x, x)
                max_y = max(max_y, y)
                min_y = min(min_y, y)

            strokes.append(stroke)

        dimensions = Rectangle(Point2D(min_x, min_y), max_x - min_x + 1, max_y - min_y + 1)
        return Symbol(content, strokes, symbol_name, dimensions)

    def draw_into_bitmap(self, export_file_name: str, stroke_thickness: int, margin: int, destination_width: int,
                         destination_height: int, draw_with_staff_lines=False) -> (int, int):
        width = self.dimensions.width + 2 * margin
        height = self.dimensions.height + 2 * margin
        width_offset_for_centering = (destination_width - width) / 2
        height_offset_for_centering = (destination_height - height) / 2
        offset = Point2D(self.dimensions.origin.x - margin - width_offset_for_centering,
                         self.dimensions.origin.y - margin - height_offset_for_centering)

        image = Image.new('RGB', (destination_width, destination_height), "white")  # create a new black image
        draw = ImageDraw.Draw(image)
        black = (0, 0, 0)

        for stroke in self.strokes:
            for i in range(0, len(stroke) - 1):
                start_point = self.subtract_offset(stroke[i], offset)
                end_point = self.subtract_offset(stroke[i + 1], offset)
                draw.line((start_point.x, start_point.y, end_point.x, end_point.y), black, stroke_thickness)

        if draw_with_staff_lines:
            self.draw_staff_lines_into_image(image, stroke_thickness)
            file_name, extension = os.path.splitext(os.path.basename(export_file_name))
            path = os.path.dirname(export_file_name)
            vertical_offset = 88
            export_file_name = "{0}_offset_{1}{2}".format(os.path.join(path,file_name), vertical_offset, extension)

        image.save(export_file_name)

    def draw_staff_lines_into_image(self, image: Image, stroke_thickness: int, staff_line_spacing: int = 14,
                                    vertical_offset=88):
        black = (0, 0, 0)
        width = image.width
        draw = ImageDraw.Draw(image)

        for i in range(5):
            y = vertical_offset + i * staff_line_spacing
            draw.line((0, y, width, y), black, stroke_thickness)

    def draw_staff_lines_into_bitmap(self, file_name: str, stroke_thickness: int, staff_line_spacing: int = 14,
                                     vertical_offset=88):
        image = Image.open(file_name)
        self.draw_staff_lines_into_image(image, stroke_thickness, staff_line_spacing, vertical_offset)

        export_file_name = "{0}_offset_{1}.png".format(os.path.splitext(os.path.basename(file_name))[0],
                                                       vertical_offset)
        image.save(export_file_name)

    def subtract_offset(self, a: Point2D, b: Point2D) -> Point2D:
        return Point2D(a.x - b.x, a.y - b.y)
