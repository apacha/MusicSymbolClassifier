import argparse
import os
from glob import glob
from typing import List

import sys

from datasets.ExportPath import ExportPath
from datasets.Symbol import Symbol


class HomusImageGenerator:
    @staticmethod
    def create_images(raw_data_directory: str,
                      destination_directory: str,
                      stroke_thicknesses: List[int] = [3],
                      width: int = 128,
                      height: int = 224,
                      staff_line_spacing: int = 14,
                      staff_line_vertical_offsets: List[int] = None) -> dict:
        all_symbol_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.txt'))]

        staff_line_multiplier = 1
        if staff_line_vertical_offsets is not None:
            staff_line_multiplier = len(staff_line_vertical_offsets)

        total_number_of_symbols = len(all_symbol_files) * len(stroke_thicknesses) * staff_line_multiplier
        output = "Generating {0} images with {1} symbols in {2} different stroke thicknesses ({3})".format(
            total_number_of_symbols, len(all_symbol_files), len(stroke_thicknesses), stroke_thicknesses)

        if staff_line_vertical_offsets is not None:
            output += " and with staff-lines with {0} different offsets from the top ({1})".format(
                staff_line_multiplier, staff_line_vertical_offsets)

        output += "\nIn directory {0}".format(os.path.abspath(destination_directory))
        print(output)
        current_symbol = 0
        bounding_boxes = dict()

        for symbol_file in all_symbol_files:
            with open(symbol_file) as file:
                content = file.read()

            symbol = Symbol.initialize_from_string(content)

            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = os.path.splitext(os.path.basename(symbol_file))[0]

            for stroke_thickness in stroke_thicknesses:
                export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension,
                                         stroke_thickness, 'png')
                symbol.draw_into_bitmap(export_path, stroke_thickness, 0, width,
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
        default="../data/raw",
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
    parser.add_argument("--width", default="128", type=int, help="Width of the generated images in pixel")
    parser.add_argument("--height", default="224", type=int, help="Height of the generated images in pixel")
    parser.add_argument("--staff_line_spacing", default="14", type=int, help="Spacing between two staff-lines in pixel")

    flags, unparsed = parser.parse_known_args()

    HomusImageGenerator.create_images(flags.raw_dataset_directory,
                                      flags.image_dataset_directory,
                                      [int(s) for s in flags.stroke_thicknesses.split(',')],
                                      flags.width,
                                      flags.height,
                                      flags.staff_line_spacing,
                                      [int(o) for o in flags.offsets.split(',')])
