import argparse
import json

import os

import shutil
from omrdatasettools.converters.ImageColorInverter import ImageColorInverter
from omrdatasettools.downloaders.FornesMusicSymbolsDatasetDownloader import FornesMusicSymbolsDatasetDownloader
from tqdm import tqdm


class FornesMusicSymbolsImagePreparer(object):
    def __init__(self) -> None:
        super().__init__()
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))

    def prepare_dataset(self, raw_dataset_directory, image_dataset_directory):
        image_inverter = ImageColorInverter()
        image_inverter.invert_images(raw_dataset_directory, "*.bmp")

        with open(os.path.join(self.path_of_this_file, "FornesMusicSymbolsBrokenSymbols.json")) as file:
            broken_symbols = json.load(file)
        with open(os.path.join(self.path_of_this_file, "FornesMusicSymbolsNameMapping.json")) as file:
            class_name_mapping = json.load(file)

        image_directories = [dir for dir in os.listdir(raw_dataset_directory) if
                             os.path.isdir(os.path.join(raw_dataset_directory, dir))]

        print("Copying images into respective class folders ...")

        for symbol_class in tqdm(image_directories):
            destination_class_name = class_name_mapping[symbol_class]
            source_folder = os.path.join(raw_dataset_directory, symbol_class)
            destination_folder = os.path.join(image_dataset_directory, destination_class_name)
            os.makedirs(destination_folder, exist_ok=True)
            all_png_images = [i for i in os.listdir(source_folder) if i.endswith(".png") and i not in broken_symbols]
            for image in all_png_images:
                shutil.copy(os.path.join(source_folder, image), destination_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/fornes_raw",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the images will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset_downloader = FornesMusicSymbolsDatasetDownloader()
    dataset_downloader.download_and_extract_dataset(flags.raw_dataset_directory)

    dataset_preparer = FornesMusicSymbolsImagePreparer()
    dataset_preparer.prepare_dataset(flags.raw_dataset_directory, flags.image_dataset_directory)
