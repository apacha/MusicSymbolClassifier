import argparse
import os

from datasets.Dataset import Dataset


class HomusDatasetDownloader(Dataset):
    """ Downloads the HOMUS dataset (V-2.0)
        http://grfia.dlsi.ua.es/homus/
        License unspecified
    """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        """
        super().__init__(destination_directory)

    def get_dataset_download_url(self) -> str:
        return "https://owncloud.tuwien.ac.at/index.php/s/5qVjo9HGGN1bN4I/download"

    def get_dataset_filename(self) -> str:
        return "HOMUS-2.0.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading HOMUS Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting HOMUS Dataset...")
        self.extract_dataset(self.destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/homus_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = HomusDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
