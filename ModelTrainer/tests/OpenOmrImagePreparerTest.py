import os
from glob import glob

from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset

from datasets.OpenOmrImagePreparer import OpenOmrImagePreparer


class OpenOmrImagePreparerTest:
    def test_download_and_prepare_dataset(self, tmp_path):
        # Arrange
        dataset_downloader = Downloader()
        expected_number_of_images = 503

        # Act
        dataset_downloader.download_and_extract_dataset(OmrDataset.OpenOmr, str(tmp_path / "open_omr_raw2"))
        image_generator = OpenOmrImagePreparer()
        image_generator.prepare_dataset(str(tmp_path / "open_omr_raw2"), str(tmp_path / "open_omr_image2"))
        all_image_files = [y for x in os.walk(tmp_path / "open_omr_image2") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_images = len(all_image_files)

        # Assert
        assert expected_number_of_images == actual_number_of_images
