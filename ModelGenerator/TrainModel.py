import datetime
import os
from time import time

import argparse
import numpy as np
import shutil
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator

from TrainingHistoryPlotter import TrainingHistoryPlotter
from datasets.AdditionalDataset import AdditionalDataset
from datasets.DatasetSplitter import DatasetSplitter
from datasets.MuscimaDataset import MuscimaDataset
from datasets.PascalVocDataset import PascalVocDataset
from models.ConfigurationFactory import ConfigurationFactory


def train_model(dataset_directory: str,
                model_name: str,
                show_plot_after_training: bool,
                delete_and_recreate_dataset_directory: bool):
    print("Downloading and extracting datasets...")

    if delete_and_recreate_dataset_directory:
        print("Deleting dataset directory and creating it anew")
        shutil.rmtree(dataset_directory)

        pascal_voc_dataset = PascalVocDataset(dataset_directory)
        pascal_voc_dataset.download_and_extract_dataset()
        muscima_dataset = MuscimaDataset(dataset_directory)
        muscima_dataset.download_and_extract_dataset()
        additional_dataset = AdditionalDataset(dataset_directory)
        additional_dataset.download_and_extract_dataset()

        dataset_splitter = DatasetSplitter(dataset_directory, dataset_directory)
        dataset_splitter.split_images_into_training_validation_and_test_set()

    print("Training on dataset...")
    start_time = time()

    training_configuration = ConfigurationFactory.get_configuration_by_name(model_name)
    img_rows, img_cols = training_configuration.data_shape[0], training_configuration.data_shape[1]
    number_of_pixels_shift = training_configuration.number_of_pixel_shift

    train_generator = ImageDataGenerator(horizontal_flip=True,
                                         rotation_range=10,
                                         width_shift_range=number_of_pixels_shift / img_rows,
                                         height_shift_range=number_of_pixels_shift / img_cols,
                                         )
    training_data_generator = train_generator.flow_from_directory(os.path.join(dataset_directory, "training"),
                                                                  target_size=(img_cols, img_rows),
                                                                  batch_size=training_configuration.training_minibatch_size,
                                                                  )
    training_steps_per_epoch = np.math.ceil(training_data_generator.samples / training_data_generator.batch_size)

    validation_generator = ImageDataGenerator()
    validation_data_generator = validation_generator.flow_from_directory(os.path.join(dataset_directory, "validation"),
                                                                         target_size=(img_cols, img_rows),
                                                                         batch_size=training_configuration.training_minibatch_size)
    validation_steps_per_epoch = np.math.ceil(validation_data_generator.samples / validation_data_generator.batch_size)

    test_generator = ImageDataGenerator()
    test_data_generator = test_generator.flow_from_directory(os.path.join(dataset_directory, "test"),
                                                             target_size=(img_cols, img_rows),
                                                             batch_size=training_configuration.training_minibatch_size)
    test_steps_per_epoch = np.math.ceil(test_data_generator.samples / test_data_generator.batch_size)

    model = training_configuration.classifier()
    model.summary()

    print("Model {0} loaded.".format(training_configuration.name()))
    print(training_configuration.summary())

    best_model_path = "{0}.h5".format(training_configuration.name())

    model_checkpoint = ModelCheckpoint(best_model_path, monitor="val_acc", save_best_only=True, verbose=1)
    early_stop = EarlyStopping(monitor='val_acc',
                               patience=training_configuration.number_of_epochs_before_early_stopping,
                               verbose=1)
    learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                                patience=training_configuration.number_of_epochs_before_reducing_learning_rate,
                                                verbose=1,
                                                factor=training_configuration.learning_rate_reduction_factor,
                                                min_lr=training_configuration.minimum_learning_rate)
    history = model.fit_generator(
            generator=training_data_generator,
            steps_per_epoch=training_steps_per_epoch,
            epochs=training_configuration.number_of_epochs,
            callbacks=[model_checkpoint, early_stop, learning_rate_reduction],
            validation_data=validation_data_generator,
            validation_steps=validation_steps_per_epoch
    )

    print("Loading best model from check-point and testing...")
    # For some models, loading the model directly does not work, but loading the weights does
    # (see https://github.com/fchollet/keras/issues/4044#issuecomment-254921595)
    # best_model = keras.models.load_model(best_model_path)
    best_model = training_configuration.classifier()
    best_model.load_weights(best_model_path)

    evaluation = best_model.evaluate_generator(test_data_generator, steps=test_steps_per_epoch)

    print(best_model.metrics_names)
    print("Loss : ", evaluation[0])
    print("Accuracy : ", evaluation[1])
    print("Error : ", 1 - evaluation[1])

    TrainingHistoryPlotter.plot_history(history,
                                        "Results-{0}-{1}.png".format(training_configuration.name(),
                                                                     datetime.date.today()),
                                        show_plot=show_plot_after_training)

    end_time = time()
    print("Execution time: %.1fs" % (end_time - start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument(
            "--dataset_directory",
            type=str,
            default="data",
            help="The directory, that is used for storing the images during training")
    parser.add_argument(
            "--model_name",
            type=str,
            default="vgg",
            help="The model used for training the network. Currently allowed values are \'simple\' or \'vgg\'")
    parser.add_argument(
            "--show_plot_after_training",
            nargs="?",
            const=True,
            type="bool",
            default=True,
            help="Whether to show a plot with the accuracies after training or not.")
    parser.add_argument(
            "--delete_and_recreate_dataset_directory",
            nargs="?",
            const=True,
            type="bool",
            default=True,
            help="Whether to delete and recreate the dataset-directory (by downloading the appropriate "
                 "files from the internet) or simply use whatever data currently is inside of that directory.")

    flags, unparsed = parser.parse_known_args()

    train_model(flags.dataset_directory,
                flags.model_name,
                flags.show_plot_after_training,
                flags.delete_and_recreate_dataset_directory)
