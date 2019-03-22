import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders.OpenOmrDatasetDownloader import OpenOmrDatasetDownloader

from datasets.OpenOmrImagePreparer import OpenOmrImagePreparer


class OpenOmrImagePreparerTest(unittest.TestCase):
    def test_download_and_prepare_dataset(self):
        # Arrange
        datasetDownloader = OpenOmrDatasetDownloader()
        expected_number_of_images = 503

        # Act
        datasetDownloader.download_and_extract_dataset("temp/open_omr_raw2")
        image_generator = OpenOmrImagePreparer()
        image_generator.prepare_dataset("temp/open_omr_raw2", "temp/open_omr_image2")
        all_image_files = [y for x in os.walk("temp/open_omr_image2") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_images = len(all_image_files)

        # Assert
        self.assertEqual(expected_number_of_images, actual_number_of_images)

        # Cleanup
        os.remove(datasetDownloader.get_dataset_filename())
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
