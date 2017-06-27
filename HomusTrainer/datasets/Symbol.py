import os
from typing import List

import sys

from PIL import ImageDraw
from sympy import Point2D
from PIL import Image

from datasets.ExportPath import ExportPath
from datasets.Rectangle import Rectangle


class Symbol:
    def __init__(self, content: str, strokes: List[List[Point2D]], symbol_class: str, dimensions: Rectangle) -> None:
        super().__init__()
        self.dimensions = dimensions
        self.symbol_class = symbol_class
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

    def draw_into_bitmap(self, export_path: ExportPath, stroke_thickness: int, margin: int, destination_width: int,
                         destination_height: int, staff_line_spacing: int = 14,
                         staff_line_vertical_offsets: List[int] = None, bounding_boxes: dict = None):
        """

        :param bounding_boxes: The dictionary into which the bounding-boxes will be added of each generated image
        :param export_path:
        :param stroke_thickness:
        :param margin:
        :param destination_width:
        :param destination_height:
        :param staff_line_spacing:
        :param staff_line_vertical_offsets: Offsets used for drawing staff-lines. If None provided, no staff-lines will
                  be drawn if multiple integers are provided, multiple images will be generated
        """
        width = self.dimensions.width + 2 * margin
        height = self.dimensions.height + 2 * margin
        width_offset_for_centering = (destination_width - width) / 2
        height_offset_for_centering = (destination_height - height) / 2
        offset = Point2D(self.dimensions.origin.x - margin - width_offset_for_centering,
                         self.dimensions.origin.y - margin - height_offset_for_centering)

        image_without_staff_lines = Image.new('RGB', (destination_width, destination_height),
                                              "white")  # create a new black image_without_staff_lines
        draw = ImageDraw.Draw(image_without_staff_lines)
        black = (0, 0, 0)

        for stroke in self.strokes:
            for i in range(0, len(stroke) - 1):
                start_point = self.subtract_offset(stroke[i], offset)
                end_point = self.subtract_offset(stroke[i + 1], offset)
                draw.line((start_point.x, start_point.y, end_point.x, end_point.y), black, stroke_thickness)

        location = self.subtract_offset(self.dimensions.origin, offset)
        bounding_box_in_image = Rectangle(location, self.dimensions.width, self.dimensions.height)
        # self.draw_bounding_box(draw, location)

        del draw

        if staff_line_vertical_offsets is not None:
            for staff_line_vertical_offset in staff_line_vertical_offsets:
                image_with_staff_lines = image_without_staff_lines.copy()
                self.draw_staff_lines_into_image(image_with_staff_lines, stroke_thickness,
                                                 staff_line_spacing, staff_line_vertical_offset)
                file_name_with_offset = export_path.get_full_path(staff_line_vertical_offset)
                image_with_staff_lines.save(file_name_with_offset)
                image_with_staff_lines.close()
                bounding_boxes[file_name_with_offset] = bounding_box_in_image
        else:
            image_without_staff_lines.save(export_path.get_full_path())

        image_without_staff_lines.close()

    def draw_bounding_box(self, draw, location):
        red = (255, 0, 0)
        draw.rectangle(
            (location.x, location.y, location.x + self.dimensions.width, location.y + self.dimensions.height),
            fill=None, outline=red)

    @staticmethod
    def draw_staff_lines_into_image(image: Image,
                                    stroke_thickness: int,
                                    staff_line_spacing: int = 14,
                                    vertical_offset=88):
        black = (0, 0, 0)
        width = image.width
        draw = ImageDraw.Draw(image)

        for i in range(5):
            y = vertical_offset + i * staff_line_spacing
            draw.line((0, y, width, y), black, stroke_thickness)
        del draw

    @staticmethod
    def subtract_offset(a: Point2D, b: Point2D) -> Point2D:
        return Point2D(a.x - b.x, a.y - b.y)
