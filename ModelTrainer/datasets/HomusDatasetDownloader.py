import os
import shutil
import zipfile

import argparse
import numpy

from datasets.Dataset import Dataset


class HomusDatasetDownloader(Dataset):
    """ Downloads the HOMUS dataset (V-2.0) """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be placed.        
        """
        super().__init__(destination_directory)
        self.url = "https://owncloud.tuwien.ac.at/index.php/s/5qVjo9HGGN1bN4I/download"
        self.dataset_filename = "HOMUS-2.0.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.dataset_filename):
            print("Downloading HOMUS Dataset...")
            self.download_file(self.url, self.dataset_filename)

        print("Extracting HOMUS Dataset...")
        self.extract_dataset(self.destination_directory)

    def extract_dataset(self, absolute_path_to_temp_folder: str):
        archive = zipfile.ZipFile(self.dataset_filename, "r")
        archive.extractall(absolute_path_to_temp_folder)
        archive.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = HomusDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
