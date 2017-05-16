import os
import random
import shutil
from typing import List

import numpy


class DatasetSplitter:
    """ The abstract base class for the datasets used to train the model """

    def __init__(self,
                 source_directory: str,
                 destination_directory: str):
        """

        :param source_directory: The root directory, where all images currently reside.
            Must have two sub-folders called scores and other.
        :param destination_directory: The root directory, into which the data will be placed.
            Inside of this directory, the following structure contains the data:

         directory
         |- training
         |   |- other
         |   |- scores
         |
         |- validation
         |   |- other
         |   |- scores
         |
         |- test
         |   |- other
         |   |- scores

        """
        self.source_directory = source_directory
        self.destination_directory = os.path.abspath(destination_directory)

    def get_random_training_validation_and_test_sample_indices(self,
                                                               dataset_size: int,
                                                               validation_percentage: float = 0.1,
                                                               test_percentage: float = 0.1,
                                                               seed:int = 0) -> (List[int], List[int], List[int]):
        """
        Returns a reproducible set of random sample indices from the entire dataset population
        :param dataset_size: The population size
        :param validation_percentage: the percentage of the entire population size that should be used for validation
        :param test_percentage: the percentage of the entire population size that should be used for testing
        :param seed: An arbitrary seed that can be used to obtain repeatable pseudo-random indices
        :return: A triple of three list, containing indices of the training, validation and test sets
        """
        random.seed(seed)
        all_indices = range(0, dataset_size)
        validation_sample_size = int(dataset_size * validation_percentage)
        test_sample_size = int(dataset_size * test_percentage)
        validation_sample_indices = random.sample(all_indices, validation_sample_size)
        test_sample_indices = random.sample((set(all_indices) - set(validation_sample_indices)), test_sample_size)
        training_sample_indices = list(set(all_indices) - set(validation_sample_indices) - set(test_sample_indices))
        return training_sample_indices, validation_sample_indices, test_sample_indices

    def split_images_into_training_validation_and_test_set(self):
        print("Splitting data into training, validation and test sets...")

        for image_class in ["other", "scores"]:
            path_to_images_of_class = os.path.join(self.source_directory, image_class)
            number_of_images_in_class = len(os.listdir(path_to_images_of_class))
            training_sample_indices, validation_sample_indices, test_sample_indices = \
                self.get_random_training_validation_and_test_sample_indices(number_of_images_in_class)

            self.copy_files(image_class, path_to_images_of_class, training_sample_indices, "training")
            self.copy_files(image_class, path_to_images_of_class, validation_sample_indices, "validation")
            self.copy_files(image_class, path_to_images_of_class, test_sample_indices, "test")

    def copy_files(self, image_class, path_to_images_of_class, sample_indices, name_of_split):
        files = numpy.array(os.listdir(path_to_images_of_class))[sample_indices]
        destination_path = os.path.join(self.destination_directory, name_of_split, image_class)
        os.makedirs(destination_path, exist_ok=True)
        print("Copying {0} {2} images of {1}...".format(len(files), image_class, name_of_split))
        for image in files:
            shutil.copy(os.path.join(path_to_images_of_class, image), destination_path)


# dataset_splitter = DatasetSplitter("C:\\Users\\Alex\\Repositories\\MusicScoreClassifier\\ModelGenerator\\data",
#                                    "C:\\Users\\Alex\\Repositories\\MusicScoreClassifier\\ModelGenerator\\data")
# dataset_splitter.split_images_into_training_validation_and_test_set()