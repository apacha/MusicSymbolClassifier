import os
import shutil
import unittest
from glob import glob

from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset

from datasets.MuscimaPlusPlusImageGenerator2 import MuscimaPlusPlusImageGenerator2


class MuscimaPlusPlusImageGeneratorTest(unittest.TestCase):

    def test_download_extract_and_render_training_symbols(self):
        # Arrange
        dataset_downloader = Downloader()
        expected_number_of_images = 55574

        # Act
        dataset_downloader.download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_V1, "temp/muscima_pp_raw")
        image_generator = MuscimaPlusPlusImageGenerator2()
        image_generator.extract_symbols_for_training("temp/muscima_pp_raw", "temp/muscima_img")
        all_image_files = [y for x in os.walk("temp/muscima_img") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_images = len(all_image_files)

        # Assert
        self.assertEqual(expected_number_of_images, actual_number_of_images)

        # Cleanup
        os.remove(OmrDataset.MuscimaPlusPlus_V1.get_dataset_filename())
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
