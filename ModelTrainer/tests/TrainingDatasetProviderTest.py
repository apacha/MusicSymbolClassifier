import os
import shutil
from glob import glob
from pathlib import Path

from datasets.TrainingDatasetProvider import TrainingDatasetProvider


class TrainingDatasetProviderTest:
    def test_download_and_prepare_dataset(self, tmp_path: Path):
        # Arrange
        dataset_provider = TrainingDatasetProvider(str(tmp_path))
        datasets = ["homus", "rebelo1", "rebelo2", "printed", "audiveris", "muscima_pp", "fornes", "openomr"]
        expected_number_of_images = 80405
        expected_number_of_classes = 84

        # Act
        dataset_provider.recreate_and_prepare_datasets_for_training(datasets, 80, 80, True, [3], 14, [], False)

        # Assert
        all_image_files = [y for x in os.walk(tmp_path / "images") for y in glob(os.path.join(x[0], '*.png'))]
        all_classes = os.listdir(tmp_path / "images")
        actual_number_of_classes = len(all_classes)
        actual_number_of_images = len(all_image_files)

        assert expected_number_of_images == actual_number_of_images
        assert expected_number_of_classes == actual_number_of_classes
