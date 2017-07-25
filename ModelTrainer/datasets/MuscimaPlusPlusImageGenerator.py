import argparse
import os
from glob import glob

from PIL import Image
from muscima.io import parse_cropobject_list
from datasets.ExportPath import ExportPath


class MuscimaPlusPlusImageGenerator:
    def __init__(self) -> None:
        super().__init__()

    def extract_symbols(self, raw_data_directory: str, destination_directory: str):
        """
        Extracts the symbols from the raw XML documents and generates individual symbols from the masks

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        """
        print("Extracting Symbols from Muscima++ Dataset...")

        raw_data_directory = os.path.join(raw_data_directory, "v0.9", "data", "cropobjects")
        xml_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.xml'))]

        for xml_file in xml_files:
            self.__extract_and_draw_crop_objects(xml_file, destination_directory)

    def __extract_and_draw_crop_objects(self, xml_file: str, destination_directory: str):
        # e.g., xml_file = 'data/muscima_pp/v0.9/data/cropobjects/CVC-MUSCIMA_W-01_N-10_D-ideal.xml'
        crop_objects = parse_cropobject_list(xml_file)

        for crop_object in crop_objects:
            symbol_class = crop_object.clsname
            # Some classes have "-symbols in their name, that we just remove
            symbol_class = symbol_class.replace('"', '')
            # Make a copy of the mask to not temper with the original data
            mask = crop_object.mask.copy()
            # We want to draw black symbols on white canvas. The mask encodes foreground pixels
            # that we are interested in with a 1 and background pixels with a 0 and stores those values in
            # an uint8 numpy array. To use Image.fromarray, we have to generate a greyscale mask, where
            # white pixels have the value 255 and black pixels have the value 0. To achieve this, we simply
            # subtract one from each uint, and by exploiting the underflow of the uint we get the following mapping:
            # 0 (background) => 255 (white) and 1 (foreground) => 0 (black) which is exactly what we wanted.
            mask -= 1
            image = Image.fromarray(mask, mode="L")

            target_directory = os.path.join(destination_directory, symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            export_path = ExportPath(destination_directory, symbol_class, crop_object.uid)
            image.save(export_path.get_full_path())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/muscima_pp_raw",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the generated bitmaps will be created")

    flags, unparsed = parser.parse_known_args()

    muscima_pp_image_generator = MuscimaPlusPlusImageGenerator()
    muscima_pp_image_generator.extract_symbols(flags.raw_dataset_directory, flags.image_dataset_directory)
