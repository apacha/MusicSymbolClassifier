import argparse
import os
from glob import glob

from datasets.Symbol import Symbol


class HomusImageGenerator:
    @staticmethod
    def create_images(raw_data_directory: str, destination_directory: str):
        all_symbol_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.txt'))]

        for symbol_file in all_symbol_files:
            with open(symbol_file) as file:
                content = file.read()

            symbol = Symbol.initialize_from_string(content)

            stroke_thickness = 3
            width = 128
            height = 224

            target_directory = os.path.join(destination_directory, symbol.symbol_name)
            os.makedirs(target_directory, exist_ok=True)

            file_name = os.path.splitext(os.path.basename(symbol_file))[0]
            export_file_name = "{0}_{1}.png".format(file_name, stroke_thickness)

            symbol.draw_into_bitmap(os.path.join(target_directory,export_file_name), stroke_thickness, 0, width, height)
        pass


if __name__ == "__main__":
    HomusImageGenerator.create_images("../data/raw", "../data/images")
