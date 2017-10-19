import os

import math
from typing import Optional

from sklearn.utils import class_weight
import numpy


class ClassWeightCalculator:
    def calculate_class_weights(self, image_dataset_directory: str, method: str = "skBalanced",
                                class_indices: dict = None) -> Optional[dict]:
        """
        Calculates appropriate class weights for the given dataset. Images with higher occurence will get a lower
        weight, than classes with only a few instances.

        -) method=None will return None for not using any class_weights
        -) method="simple" will return 1 / sqrt(number_of_elements_in_class) as weight per class
        -) method="skBalanced" will use sklearn to compute balanced weights

        :param class_indices: The dictionary, that contains the mapping of class names to index from the data_generator
        :param image_dataset_directory:
        :param method: string constant, either None, "skBalanced" or "simple"
        :return:
        """

        if method is None:
            return None

        if method not in ['simple', 'skBalance']:
            raise ValueError("Method must either be None, or one of the strings 'simple' or 'skBalance', "
                             "but provided was {0}.".format(method))

        classes = os.listdir(image_dataset_directory)
        try:
            classes.remove('training')
            classes.remove('test')
            classes.remove('validation')
        except ValueError:
            pass

        number_of_elements_per_class = dict()
        class_weights = dict()

        for class_name in classes:
            class_folder = os.path.join(image_dataset_directory, class_name)
            number_of_elements = len(os.listdir(class_folder))
            number_of_elements_per_class[class_name] = number_of_elements
            class_weights[class_name] = 1 / math.sqrt(number_of_elements)

        if method is "simple":
            pass
        else:
            # y simulates the actual data by repeating an instance of the class-name per actual instance,
            # e.g. ['1-8-Time' '1-8-Time' '12-8-Time' ..., 'Whole-Note' 'Whole-Note' 'Whole-Note']
            y = numpy.repeat(classes, list(number_of_elements_per_class.values()))

            balanced_class_weights = class_weight.compute_class_weight('balanced', classes, y)
            class_weights = dict(zip(classes, balanced_class_weights))

        class_weights_with_indices = dict()

        # Keras does not expect a dictionary with class-names as keys, but with class-indices as keys of the dictionary,
        # therefore we have to recreate the dicitionary.
        for class_name in class_weights.keys():
            class_weights_with_indices[class_indices[class_name]] = class_weights[class_name]

        return class_weights_with_indices


if __name__ == "__main__":
    class_weight_calculator = ClassWeightCalculator()
    class_weights_simple = class_weight_calculator.calculate_class_weights("data/images", "simple")
    class_weights_balanced = class_weight_calculator.calculate_class_weights("data/images", "balanced")
    print(class_weights_simple)
    print(class_weights_balanced)
