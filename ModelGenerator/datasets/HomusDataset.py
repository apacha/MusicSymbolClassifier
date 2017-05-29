import os
import shutil
import zipfile

import argparse
import numpy

from datasets.Dataset import Dataset


class AdditionalDataset(Dataset):
    """ Loads images from a custom directory and splits them into train and validation
        directories with a random generator """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be placed.        
        """
        super().__init__(destination_directory)
        self.url = "https://owncloud.tuwien.ac.at/index.php/s/JHzEMlwCSw8lTFp/download"
        self.dataset_filename = "MusicScoreClassificationDataset.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.dataset_filename):
            print("Downloading Additional Dataset...")
            self.download_file(self.url, self.dataset_filename)

        print("Extracting Additional Dataset...")
        absolute_path_to_temp_folder = os.path.abspath(os.path.join(".", "temp"))
        self.extract_dataset_into_temp_folder(absolute_path_to_temp_folder)
        self.copy_images_from_temp_directory_into_destination_directory(absolute_path_to_temp_folder)
        self.clean_up_temp_directory(absolute_path_to_temp_folder)

    def copy_images_from_temp_directory_into_destination_directory(self, absolute_path_to_temp_folder: str):
        print("Copying additional images from {0} and its subdirectories".format(absolute_path_to_temp_folder))
        path_to_all_files = [os.path.join(absolute_path_to_temp_folder, "scores", file) for file in
                             os.listdir(os.path.join(absolute_path_to_temp_folder, "scores"))]
        destination_score_image = os.path.join(self.destination_directory, "scores")
        os.makedirs(destination_score_image, exist_ok=True)
        print("Copying {0} score images...".format(len(path_to_all_files)))
        for score_image in path_to_all_files:
            shutil.copy(score_image, destination_score_image)
        path_to_all_files = [os.path.join(absolute_path_to_temp_folder, "other", file) for file in
                             os.listdir(os.path.join(absolute_path_to_temp_folder, "other"))]
        destination_other_image = os.path.join(self.destination_directory, "other")
        os.makedirs(destination_other_image, exist_ok=True)
        print("Copying {0} other images...".format(len(path_to_all_files)))
        for other_image in path_to_all_files:
            shutil.copy(other_image, destination_other_image)

    def extract_dataset_into_temp_folder(self, absolute_path_to_temp_folder: str):
        archive = zipfile.ZipFile(self.dataset_filename, "r")
        archive.extractall(absolute_path_to_temp_folder)
        archive.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--dataset_directory",
            type=str,
            default="../data",
            help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = AdditionalDataset(flags.dataset_directory)
    dataset.download_and_extract_dataset()
