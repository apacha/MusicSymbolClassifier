import os
import zipfile
import shutil

import argparse

from datasets.Dataset import Dataset


class MuscimaDataset(Dataset):
    """ This dataset contains the Musicma Handwritten music scores database which consists of 
        1000 handwritten music scores from http://www.cvc.uab.es/cvcmuscima/index_database.html """

    def __init__(self, destination_directory: str):
        super().__init__(destination_directory)
        self.url = "http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_WI.zip"
        self.dataset_filename = "CVCMUSCIMA_WI.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.dataset_filename):
            print("Downloading Muscima Dataset...")
            self.download_file(self.url)

        print("Extracting Muscima Dataset...")
        self.extract_dataset_into_temp_folder()
        absolute_image_directory = os.path.abspath(os.path.join(self.destination_directory, "scores"))
        self.copy_images_from_subdirectories_into_single_directory(absolute_image_directory)
        self.clean_up_temp_directory(os.path.abspath(os.path.join(".", "temp")))

    def extract_dataset_into_temp_folder(self):
        archive = zipfile.ZipFile(self.dataset_filename, "r")
        archive.extractall("temp")
        archive.close()

    @staticmethod
    def copy_images_from_subdirectories_into_single_directory(absolute_image_directory: str) -> str:
        os.makedirs(absolute_image_directory, exist_ok=True)
        relative_path_to_writers = os.path.join(".", "temp", "CVCMUSCIMA_WI", "PNG_GT_Gray")
        absolute_path_to_writers = os.path.abspath(relative_path_to_writers)
        writer_directories_without_mac_system_directory = [os.path.join(absolute_path_to_writers, f)
                                                           for f in os.listdir(absolute_path_to_writers)
                                                           if f != ".DS_Store"]
        for writer_directory in writer_directories_without_mac_system_directory:
            images = [os.path.join(absolute_path_to_writers, writer_directory, f)
                      for f in os.listdir(writer_directory)
                      if f != ".DS_Store"]
            for image in images:
                destination_file = os.path.join(absolute_image_directory,
                                                os.path.basename(writer_directory) + "_" + os.path.basename(image))
                shutil.copyfile(image, destination_file)

        return absolute_image_directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--dataset_directory",
            type=str,
            default="../data",
            help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    datasest = MuscimaDataset(flags.dataset_directory)
    datasest.download_and_extract_dataset()
