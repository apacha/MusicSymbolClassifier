import argparse
import json

import os
from distutils import dir_util

from omrdatasettools.downloaders.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader
from omrdatasettools.image_generators.AudiverisOmrImageGenerator import AudiverisOmrImageGenerator


class AudiverisOmrImagePreparer(object):
    def __init__(self) -> None:
        super().__init__()
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))

    def prepare_dataset(self, intermediate_image_directory, image_dataset_directory):
        with open(os.path.join(self.path_of_this_file, "AudiverisOmrIgnoredClasses.json")) as file:
            ignored_classes = json.load(file)
        with open(os.path.join(self.path_of_this_file, "AudiverisOmrClassNameMapping.json")) as file:
            class_name_mapping = json.load(file)

        image_directories = os.listdir(intermediate_image_directory)

        for symbol_class in image_directories:
            if symbol_class in ignored_classes:
                continue

            destination_class_name = class_name_mapping[symbol_class]
            source_folder = os.path.join(intermediate_image_directory, symbol_class)
            destination_folder = os.path.join(image_dataset_directory, destination_class_name)
            os.makedirs(destination_folder, exist_ok=True)
            dir_util.copy_tree(source_folder, destination_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/audiveris_omr_raw",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--intermediate_image_directory",
        type=str,
        default="../data/audiveris_omr",
        help="The directory, where the raw bitmaps will be generated")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the processed bitmaps will be copied to after filtering and renaming classes")

    flags, unparsed = parser.parse_known_args()

    dataset_downloader = AudiverisOmrDatasetDownloader(flags.raw_dataset_directory)
    dataset_downloader.download_and_extract_dataset()

    # Convert the raw data into images
    image_generator = AudiverisOmrImageGenerator()
    image_generator.extract_symbols(flags.raw_dataset_directory, flags.intermediate_image_directory)

    # Actually prepare our dataset
    dataset_preparer = AudiverisOmrImagePreparer()
    dataset_preparer.prepare_dataset(flags.intermediate_image_directory, flags.image_dataset_directory)
