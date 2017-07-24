import argparse
import os
from distutils import dir_util

from datasets.Dataset import Dataset


class AudiverisOmrDatasetDownloader(Dataset):
    """ Loads and extracts the music symbols from the Audiveris OMR dataset """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        """
        super().__init__(destination_directory)

    def get_dataset_download_url(self) -> str:
        return "https://owncloud.tuwien.ac.at/index.php/s/lSkDZxtwBLs2FOK/download"

    def get_dataset_filename(self) -> str:
        return "AudiverisOmrDataset.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Audiveris OMR dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Audiveris OMR Dataset...")
        self.extract_dataset(self.destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/audiveris_omr_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = AudiverisOmrDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
