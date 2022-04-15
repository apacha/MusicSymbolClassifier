import os
from glob import glob

from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset

from datasets.MuscimaPlusPlusImageGenerator2 import MuscimaPlusPlusImageGenerator2


class MuscimaPlusPlusImageGeneratorTest:

    def test_download_extract_and_render_training_symbols(self, tmp_path):
        # Arrange
        dataset_downloader = Downloader()
        expected_number_of_images = 44809

        # Act
        dataset_downloader.download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_V2, str(tmp_path / "muscima_pp_raw"))
        image_generator = MuscimaPlusPlusImageGenerator2()
        image_generator.extract_symbols_for_training(str(tmp_path / "muscima_pp_raw"), str(tmp_path / "muscima_img"))
        all_image_files = [y for x in os.walk(tmp_path / "muscima_img") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_images = len(all_image_files)

        # Assert
        assert expected_number_of_images == actual_number_of_images
