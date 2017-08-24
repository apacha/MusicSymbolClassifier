import os
import shutil
import unittest
from glob import glob

from datasets.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader
from datasets.Dataset import Dataset
from datasets.FornesMusicSymbolsDatasetDownloader import FornesMusicSymbolsDatasetDownloader
from datasets.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader
from datasets.OpenOmrDatasetDownloader import OpenOmrDatasetDownloader
from datasets.PrintedMusicSymbolsDatasetDownloader import PrintedMusicSymbolsDatasetDownloader
from datasets.RebeloMusicSymbolDataset1Downloader import RebeloMusicSymbolDataset1Downloader
from datasets.RebeloMusicSymbolDataset2Downloader import RebeloMusicSymbolDataset2Downloader


class DatasetDownloaderTest(unittest.TestCase):
    def test_download_and_extract_rebelo1_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "Rebelo1Images"
        downloader = RebeloMusicSymbolDataset1Downloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 7940
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_rebelo2_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "Rebelo2Images"
        downloader = RebeloMusicSymbolDataset2Downloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 7307
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_printed_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "PrintedMusicSymbols"
        downloader = PrintedMusicSymbolsDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 213
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_fornes_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "FornesMusicSymbols"
        downloader = FornesMusicSymbolsDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 4092
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_audiveris_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "AudiverisRawData"
        downloader = AudiverisOmrDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 4
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_muscima_pp_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "MuscimaPlusPlus"
        downloader = MuscimaPlusPlusDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 141
        target_file_extension = "*.xml"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_openomr_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "OpenOMR"
        downloader = OpenOmrDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 503
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

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
        all_files = [y for x in os.walk(destination_directory) for y in glob(os.path.join(x[0], target_file_extension))]
        actual_number_of_files = len(all_files)
        self.assertEqual(number_of_samples_in_the_dataset, actual_number_of_files)
        self.assertTrue(os.path.exists(zip_file))

        # Cleanup
        os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
