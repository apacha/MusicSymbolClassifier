import argparse
import os
from glob import glob
from xml.etree import ElementTree

from PIL import Image, ImageOps
import numpy


class FornesImageConverter:
    def __init__(self) -> None:
        super().__init__()

    def invert_images(self, image_directory: str):
        """
        In-situ converts the white on black images of the Fornés dataset to black on white images

        :param image_directory: The directory, that contains the images
        """
        print("Converting all images of the Fornés dataset...")

        image_paths = [y for x in os.walk(image_directory) for y in glob(os.path.join(x[0], '*.bmp'))]
        for image_path in image_paths:
            white_on_black_image = Image.open(image_path).convert("L")
            black_on_white_image = ImageOps.invert(white_on_black_image)
            black_on_white_image.save(image_path[:-4] + ".png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_directory",
        type=str,
        default="../data/fornes_raw",
        help="The directory, where the original Fornés dataset can be found")

    flags, unparsed = parser.parse_known_args()

    fornes_image_converter = FornesImageConverter()
    fornes_image_converter.invert_images(flags.image_directory)
