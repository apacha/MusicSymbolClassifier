import os
import shutil
import unittest
from glob import glob

from datasets.TrainingDatasetProvider import TrainingDatasetProvider


class TrainingDatasetProviderTest(unittest.TestCase):
    def test_download_and_prepare_dataset(self):
        # Arrange
        dataset_provider = TrainingDatasetProvider("temp")
        datasets = ["homus", "rebelo1", "rebelo2", "printed", "audiveris", "muscima_pp", "fornes", "openomr"]
        expected_number_of_images = 80405
        expected_number_of_classes = 84

        # Act
        dataset_provider.recreate_and_prepare_datasets_for_training(datasets, 80, 80, True, [3], 14, [], False)

        # Assert
        all_image_files = [y for x in os.walk("temp/images") for y in glob(os.path.join(x[0], '*.png'))]
        all_classes = os.listdir("temp/images")
        actual_number_of_classes = len(all_classes)
        actual_number_of_images = len(all_image_files)

        self.assertEqual(expected_number_of_images, actual_number_of_images)
        self.assertEqual(expected_number_of_classes, actual_number_of_classes)

        # Cleanup
        all_zip_files = [y for x in os.walk(".") for y in glob(os.path.join(x[0], '*.zip'))]
        for zip_file in all_zip_files:
            os.remove(zip_file)
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
