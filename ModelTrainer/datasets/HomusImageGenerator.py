import argparse
import os
from glob import glob
from typing import List

import sys

from datasets.ExportPath import ExportPath
from datasets.HomusSymbols import HomusSymbols


class HomusImageGenerator:
    @staticmethod
    def create_images(raw_data_directory: str,
                      destination_directory: str,
                      stroke_thicknesses: List[int],
                      width: int = None,
                      height: int = None,
                      staff_line_spacing: int = 14,
                      staff_line_vertical_offsets: List[int] = None) -> dict:
        """
        Creates a visual representation of the Homus Dataset by parsing all text-files and the symbols as specified
        by the parameters by drawing lines that connect the points from each stroke of each symbol.

        Each symbol will be drawn in the center of a fixed canvas, specified by width and height.

        :param raw_data_directory: The directory, that contains the text-files that contain the textual representation of the music symbols
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        :param width: The width of the canvas, that each image will be drawn upon, regardless of the original size of
                      the symbol. Larger symbols will be cropped. If the original size of the symbol should be used,
                      provided None here.
        :param height: The height of the canvas, that each image will be drawn upon, regardless of the original size of
                       the symbol. Larger symbols will be cropped. If the original size of the symbol should be used,
                       provided None here
        :param staff_line_spacing: Number of pixels spacing between each of the five staff-lines
        :param staff_line_vertical_offsets: List of vertical offsets, where the staff-lines will be superimposed over
                                            the drawn images. If None is provided, no staff-lines will be superimposed.
                                            If multiple values are provided, multiple versions of each symbol will be
                                            generated with the appropriate staff-lines, e.g. 1-5_3_offset_70.png and
                                            1-5_3_offset_77.png for two versions of the symbol 1-5 with stroke thickness
                                            3 and staff-line offsets 70 and 77 pixels from the top.
        :return: A dictionary that contains the file-names of all generated symbols and the respective bounding-boxes
                 of each symbol.
        """
        all_symbol_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.txt'))]

        staff_line_multiplier = 1
        if staff_line_vertical_offsets is not None and staff_line_vertical_offsets:
            staff_line_multiplier = len(staff_line_vertical_offsets)

        total_number_of_symbols = len(all_symbol_files) * len(stroke_thicknesses) * staff_line_multiplier
        output = "Generating {0} images with {1} symbols in {2} different stroke thicknesses ({3})".format(
            total_number_of_symbols, len(all_symbol_files), len(stroke_thicknesses), stroke_thicknesses)

        if staff_line_vertical_offsets is not None:
            output += " and with staff-lines with {0} different offsets from the top ({1})".format(
                staff_line_multiplier, staff_line_vertical_offsets)

        if width is not None and height is not None:
            output += "\nCentrally drawn on a fixed canvas of size {0}x{1} (Width x Height)".format(width, height)

        output += "\nIn directory {0}".format(os.path.abspath(destination_directory))
        print(output)
        current_symbol = 0
        bounding_boxes = dict()

        for symbol_file in all_symbol_files:
            with open(symbol_file) as file:
                content = file.read()

            symbol = HomusSymbols.initialize_from_string(content)

            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = os.path.splitext(os.path.basename(symbol_file))[0]

            for stroke_thickness in stroke_thicknesses:
                export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension,
                                         stroke_thickness, 'png')
                if width is None and height is None:
                    symbol.draw_into_bitmap(export_path, stroke_thickness, margin=2)
                else:
                    symbol.draw_onto_canvas(export_path, stroke_thickness, 0, width,
                                        height, staff_line_spacing, staff_line_vertical_offsets, bounding_boxes)

                current_symbol += 1 * staff_line_multiplier
                if current_symbol % 10 == 0:
                    sys.stdout.write('\r')
                    sys.stdout.write("{0: >5}/{1}".format(current_symbol, total_number_of_symbols))
                    sys.stdout.flush()

        return bounding_boxes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/homus_raw",
        help="The directory, where the raw HOMUS dataset can be found (the text-files that contain the strokes)")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the generated bitmaps will be created")
    parser.add_argument("-s", "--stroke_thicknesses", dest="stroke_thicknesses", default="3",
                        help="Stroke thicknesses for drawing the generated bitmaps. May define comma-separated list "
                             "of multiple stroke thicknesses, e.g. '1,2,3'")
    parser.add_argument("-offsets", "--staff_line_vertical_offsets", dest="offsets", default="",
                        help="Optional vertical offsets in pixel for drawing the symbols with superimposed "
                             "staff-lines starting at this pixel-offset from the top. Multiple offsets possible, "
                             "e.g. '81,88,95'")
    parser.add_argument("--width", default="96", type=int, help="Width of the generated images in pixel")
    parser.add_argument("--height", default="96", type=int, help="Height of the generated images in pixel")
    parser.add_argument("--staff_line_spacing", default="14", type=int, help="Spacing between two staff-lines in pixel")

    parser.add_argument("--disable_fixed_canvas_size", dest="use_fixed_canvas",
                        action="store_false",
                        help="True, if the images should be drawn on a fixed canvas with the specified width and height."
                             "False to draw the symbols with their original sizes (each symbol might be different)")
    parser.set_defaults(use_fixed_canvas=True)

    flags, unparsed = parser.parse_known_args()

    offsets = []
    if flags.offsets != "":
        offsets = [int(o) for o in flags.offsets.split(',')]

    width, height = flags.width, flags.height
    if not flags.use_fixed_canvas:
        width, height = None, None

    HomusImageGenerator.create_images(flags.raw_dataset_directory,
                                      flags.image_dataset_directory,
                                      [int(s) for s in flags.stroke_thicknesses.split(',')],
                                      width,
                                      height,
                                      flags.staff_line_spacing,
                                      offsets)
