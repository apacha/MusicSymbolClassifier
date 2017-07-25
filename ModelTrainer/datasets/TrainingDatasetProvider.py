import os
import pickle
import shutil
from typing import List

from PIL import Image

from datasets.DatasetSplitter import DatasetSplitter
from datasets.HomusDatasetDownloader import HomusDatasetDownloader
from datasets.HomusImageGenerator import HomusImageGenerator
from datasets.ImageResizer import ImageResizer
from datasets.PrintedMusicSymbolsDatasetDownloader import PrintedMusicSymbolsDatasetDownloader
from datasets.RebeloMusicSymbolDataset1Downloader import RebeloMusicSymbolDataset1Downloader
from datasets.RebeloMusicSymbolDataset2Downloader import RebeloMusicSymbolDataset2Downloader


class TrainingDatasetProvider:
    """
    Class that provides the datasets used for training a convolutional neural network in the appropriate way.
    It deletes the existing directory, handles the downloading, creating, resizing and splitting of the
    requested datasets for a subsequent training.
    """

    def __init__(self, dataset_directory: str) -> None:
        self.dataset_directory = dataset_directory
        self.image_dataset_directory = os.path.join(dataset_directory, "images")

    def recreate_and_prepare_datasets_for_training(self, datasets: List[str], width: int, height: int,
                                                   use_fixed_canvas: bool,
                                                   stroke_thicknesses_for_generated_symbols: List[int],
                                                   staff_line_spacing: int, staff_line_vertical_offsets: List[int]) -> None:
        """
        Deletes the dataset_directory and recreates the requested datasets into that folder.
        Some datasets just need to be downloaded and extracted (e.g. PrintedMusicSymbolsDataset),
        whereas other datasets require more extensive generation operations, e.g. Homus dataset.
        """
        self.__delete_dataset_directory()
        self.__download_and_extract_datasets(datasets, width, height, use_fixed_canvas, staff_line_spacing,
                                             staff_line_vertical_offsets, stroke_thicknesses_for_generated_symbols)
        self.__resize_all_images_to_fixed_size(width, height)
        self.__split_dataset_into_training_validation_and_test_set()

    def __delete_dataset_directory(self):
        print("Deleting dataset directory {0}".format(self.dataset_directory))
        if os.path.exists(self.dataset_directory):
            shutil.rmtree(self.dataset_directory)

    def __download_and_extract_datasets(self, datasets, width, height, use_fixed_canvas, staff_line_spacing,
                                        staff_line_vertical_offsets, stroke_thicknesses_for_generated_symbols):
        if 'homus' in datasets:
            raw_dataset_directory = os.path.join(self.dataset_directory, "homus_raw")
            dataset_downloader = HomusDatasetDownloader(raw_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
            generated_image_width = width
            generated_image_height = height
            if not use_fixed_canvas:
                # If we are not using a fixed canvas, remove those arguments to allow symbols being drawn at their original shapes
                generated_image_width, generated_image_height = None, None
            bounding_boxes = HomusImageGenerator.create_images(raw_dataset_directory, self.image_dataset_directory,
                                                               stroke_thicknesses_for_generated_symbols,
                                                               generated_image_width,
                                                               generated_image_height, staff_line_spacing,
                                                               staff_line_vertical_offsets)

            bounding_boxes_cache = os.path.join(self.dataset_directory, "bounding_boxes.txt")
            with open(bounding_boxes_cache, "wb") as cache:
                pickle.dump(bounding_boxes, cache)
        if 'rebelo1' in datasets:
            dataset_downloader = RebeloMusicSymbolDataset1Downloader(self.image_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
        if 'rebelo2' in datasets:
            dataset_downloader = RebeloMusicSymbolDataset2Downloader(self.image_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
        if 'printed' in datasets:
            dataset_downloader = PrintedMusicSymbolsDatasetDownloader(self.image_dataset_directory)
            dataset_downloader.download_and_extract_dataset()

    def __resize_all_images_to_fixed_size(self, width, height):
        print("Resizing all images with the LANCZOS interpolation to {0}x{1}px (width x height).".format(width, height))
        image_resizer = ImageResizer()
        image_resizer.resize_all_images(self.image_dataset_directory, width, height, Image.LANCZOS)

    def __split_dataset_into_training_validation_and_test_set(self):
        dataset_splitter = DatasetSplitter(self.image_dataset_directory, self.image_dataset_directory)
        dataset_splitter.delete_split_directories()
        dataset_splitter.split_images_into_training_validation_and_test_set()

if __name__ == "__main__":
    training_dataset_provider = TrainingDatasetProvider("../data")
    training_dataset_provider.recreate_and_prepare_datasets_for_training(["homus", "rebelo1", "rebelo2", "printed"], 96,
                                                                         96, False, [3], 14, [])
