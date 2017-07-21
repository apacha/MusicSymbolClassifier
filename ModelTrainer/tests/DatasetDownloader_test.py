import os
import shutil
import unittest
from glob import glob

from datasets.Dataset import Dataset
from datasets.HomusDatasetDownloader import HomusDatasetDownloader
from datasets.PrintedMusicSymbolsDatasetDownloader import PrintedMusicSymbolsDatasetDownloader
from datasets.RebeloMusicSymbolDataset1Downloader import RebeloMusicSymbolDataset1Downloader
from datasets.RebeloMusicSymbolDataset2Downloader import RebeloMusicSymbolDataset2Downloader


class DatasetDownloaderTest(unittest.TestCase):
    def test_download_and_extract_homus_dataset_expect_folder_to_be_created(self):
        zip_file = "HOMUS-2.0.zip"
        number_of_samples_in_the_dataset = 15200
        destination_directory = "HOMUS"
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            HomusDatasetDownloader("."))

    def test_download_and_extract_rebelo1_dataset_expect_folder_to_be_created(self):
        # Arrange
        zip_file = "Rebelo-Music-Symbol-Dataset1.zip"
        destination_directory = "Rebelo1Images"
        number_of_samples_in_the_dataset = 7940
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            RebeloMusicSymbolDataset1Downloader(destination_directory))

    def test_download_and_extract_rebelo2_dataset_expect_folder_to_be_created(self):
        # Arrange
        zip_file = "Rebelo-Music-Symbol-Dataset2.zip"
        destination_directory = "Rebelo2Images"
        number_of_samples_in_the_dataset = 7307
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            RebeloMusicSymbolDataset2Downloader(destination_directory))

    def test_download_and_extract_printed_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        zip_file = "PrintedMusicSymbolsDataset.zip"
        destination_directory = "PrintedMusicSymbols"
        number_of_samples_in_the_dataset = 85
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            PrintedMusicSymbolsDatasetDownloader(destination_directory))

    def download_dataset_and_verify_correct_extraction(self, destination_directory: str,
                                                       number_of_samples_in_the_dataset: int,
                                                       target_file_extension: str, zip_file: str,
                                                       dataset_downloader: Dataset):
        # Arrange and Cleanup
        if os.path.exists(zip_file):
            os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)

        # Act
        dataset_downloader.download_and_extract_dataset()

        # Assert
        all_text_files = [y for x in os.walk(destination_directory) for y in
                          glob(os.path.join(x[0], target_file_extension))]
        actual_number_of_files = len(all_text_files)
        self.assertEqual(number_of_samples_in_the_dataset, actual_number_of_files)
        self.assertTrue(os.path.exists(zip_file))

        # Cleanup
        os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
