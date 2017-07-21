import unittest

import math
import numpy
import os
from glob import glob

import shutil

from datasets.HomusDatasetDownloader import HomusDatasetDownloader


class HomusDatasetDownloaderTest(unittest.TestCase):
    def test_download_and_extract_dataset_expect_folder_to_be_created(self):
        datasetDownloader = HomusDatasetDownloader(".")

        # Act
        datasetDownloader.download_and_extract_dataset()
        all_text_files = [y for x in os.walk("HOMUS") for y in glob(os.path.join(x[0], '*.txt'))]
        actual_number_of_files = len(all_text_files)

        # Assert
        self.assertTrue(os.path.exists("HOMUS.zip"))
        self.assertEqual(15200, actual_number_of_files)

        # Cleanup
        os.remove("HOMUS.zip")
        shutil.rmtree("HOMUS")


if __name__ == '__main__':
    unittest.main()
