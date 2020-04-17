import argparse
import json

import os
from distutils import dir_util

from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset
from tqdm import tqdm


class OpenOmrImagePreparer(object):
    def __init__(self) -> None:
        super().__init__()
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))

    def prepare_dataset(self, raw_dataset_directory, image_dataset_directory):
        with open(os.path.join(self.path_of_this_file, "OpenOmrIgnoredClasses.json")) as file:
            ignored_classes = json.load(file)
        with open(os.path.join(self.path_of_this_file, "OpenOmrClassNameMapping.json")) as file:
            class_name_mapping = json.load(file)

        image_directories = os.listdir(raw_dataset_directory)

        for symbol_class in tqdm(image_directories, "Copying directories..."):
            if symbol_class in ignored_classes:
                continue

            destination_class_name = class_name_mapping[symbol_class]
            source_folder = os.path.join(raw_dataset_directory, symbol_class)
            destination_folder = os.path.join(image_dataset_directory, destination_class_name)
            os.makedirs(destination_folder, exist_ok=True)
            dir_util.copy_tree(source_folder, destination_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/open_omr_raw",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the images will be copied to")

    flags, unparsed = parser.parse_known_args()

    # Download the dataset
    dataset_downloader = Downloader()
    dataset_downloader.download_and_extract_dataset(OmrDataset.OpenOmr, flags.raw_dataset_directory)

    # Actually prepare our dataset
    dataset_preparer = OpenOmrImagePreparer()
    dataset_preparer.prepare_dataset(flags.raw_dataset_directory, flags.image_dataset_directory)
