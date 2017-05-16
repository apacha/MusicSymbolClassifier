import os
import shutil
import tarfile

import argparse

from datasets.Dataset import Dataset


class PascalVocDataset(Dataset):
    """ This dataset contains the Pascal VOC 2006 challenge database which consists over 
        2618 images of ten categories from http://host.robots.ox.ac.uk/pascal/VOC/databases.html#VOC2006 """

    def __init__(self, destination_directory: str):
        super().__init__(destination_directory)
        self.url = "http://host.robots.ox.ac.uk/pascal/VOC/download/voc2006_trainval.tar"
        self.dataset_filename = "voc2006_trainval.tar"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.dataset_filename):
            print("Downloading Pascal VOC Dataset ...")
            self.download_file(self.url)

        print("Extracting Pascal VOC Dataset...")

        temp_directory = os.path.abspath(os.path.join(".", "VOCdevkit"))
        absolute_image_directory = os.path.abspath(os.path.join(".", "VOCdevkit", "VOC2006", "PNGImages"))
        try:
            self.extract_dataset_into_temp_folder(temp_directory)
            self.copy_images_from_subdirectories_into_single_directory(absolute_image_directory)
        finally:
            self.clean_up_temp_directory(temp_directory)

    def extract_dataset_into_temp_folder(self, temp_directory: str):
        print("Extracting Pascal VOC dataset into temp directory")
        if os.path.exists(temp_directory):
            shutil.rmtree(temp_directory)
        tar = tarfile.open(self.dataset_filename, "r:")
        tar.extractall()
        tar.close()

    def copy_images_from_subdirectories_into_single_directory(self, absolute_image_directory: str):
        image_destination_directory = os.path.join(self.destination_directory, "other")
        os.makedirs(image_destination_directory, exist_ok=True)

        for image in [os.path.join(absolute_image_directory, name) for name in os.listdir(absolute_image_directory)]:
            shutil.copy(image, image_destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--dataset_directory",
            type=str,
            default="../data",
            help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    datasest = PascalVocDataset(flags.dataset_directory)
    datasest.download_and_extract_dataset()
