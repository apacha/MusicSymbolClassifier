import argparse
import datetime
import os

import shutil
from typing import List

from sklearn import metrics
from time import time

import numpy
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator

from TrainingHistoryPlotter import TrainingHistoryPlotter
from datasets.DatasetSplitter import DatasetSplitter
from datasets.HomusDatasetDownloader import HomusDatasetDownloader
from datasets.HomusImageGenerator import HomusImageGenerator
from models.ConfigurationFactory import ConfigurationFactory


def train_model(dataset_directory: str,
                model_name: str,
                show_plot_after_training: bool,
                delete_and_recreate_dataset_directory: bool,
                stroke_thicknesses: List[int],
                width: int,
                height: int,
                staff_line_vertical_offsets: List[int],
                training_minibatch_size: int,
                optimizer: str,
                dynamic_learning_rate_reduction: bool):
    raw_dataset_directory = os.path.join(dataset_directory, "raw")
    image_dataset_directory = os.path.join(dataset_directory, "images")

    if delete_and_recreate_dataset_directory:
        print("Deleting dataset directory {0}".format(dataset_directory))
        if os.path.exists(dataset_directory):
            shutil.rmtree(dataset_directory)

        dataset_downloader = HomusDatasetDownloader(raw_dataset_directory)
        dataset_downloader.download_and_extract_dataset()
        HomusImageGenerator.create_images(raw_dataset_directory, image_dataset_directory,
                                          stroke_thicknesses, width, height, staff_line_vertical_offsets)

        dataset_splitter = DatasetSplitter(image_dataset_directory, image_dataset_directory)
        dataset_splitter.delete_split_directories()
        dataset_splitter.split_images_into_training_validation_and_test_set()

    print("Training on dataset...")
    start_time = time()

    training_configuration = ConfigurationFactory.get_configuration_by_name(model_name, optimizer, width, height,
                                                                            training_minibatch_size)

    train_generator = ImageDataGenerator(rotation_range=training_configuration.rotation_range,
                                         zoom_range=training_configuration.zoom_range
                                         )
    training_data_generator = train_generator.flow_from_directory(
        os.path.join(image_dataset_directory, "training"),
        target_size=(training_configuration.input_image_rows,
                     training_configuration.input_image_columns),
        batch_size=training_configuration.training_minibatch_size
    )
    training_steps_per_epoch = np.math.ceil(training_data_generator.samples / training_data_generator.batch_size)

    validation_generator = ImageDataGenerator()
    validation_data_generator = validation_generator.flow_from_directory(
        os.path.join(image_dataset_directory, "validation"),
        target_size=(
            training_configuration.input_image_rows,
            training_configuration.input_image_columns),
        batch_size=training_configuration.training_minibatch_size)
    validation_steps_per_epoch = np.math.ceil(validation_data_generator.samples / validation_data_generator.batch_size)

    test_generator = ImageDataGenerator()
    test_data_generator = test_generator.flow_from_directory(os.path.join(image_dataset_directory, "test"),
                                                             target_size=(training_configuration.input_image_rows,
                                                                          training_configuration.input_image_columns),
                                                             batch_size=training_configuration.training_minibatch_size,
                                                             shuffle=False)
    test_steps_per_epoch = np.math.ceil(test_data_generator.samples / test_data_generator.batch_size)

    model = training_configuration.classifier()
    model.summary()

    print("Model {0} loaded.".format(training_configuration.name()))
    print(training_configuration.summary())

    best_model_path = "{1}_{0}.h5".format(training_configuration.name(), datetime.date.today())

    model_checkpoint = ModelCheckpoint(best_model_path, monitor="val_acc", save_best_only=True, verbose=1)
    early_stop = EarlyStopping(monitor='val_acc',
                               patience=training_configuration.number_of_epochs_before_early_stopping,
                               verbose=1)
    learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                                patience=training_configuration.number_of_epochs_before_reducing_learning_rate,
                                                verbose=1,
                                                factor=training_configuration.learning_rate_reduction_factor,
                                                min_lr=training_configuration.minimum_learning_rate)
    if dynamic_learning_rate_reduction:
        callbacks = [model_checkpoint, early_stop, learning_rate_reduction]
    else:
        print("Learning-rate reduction on Plateau disabled")
        callbacks = [model_checkpoint, early_stop]

    history = model.fit_generator(
        generator=training_data_generator,
        steps_per_epoch=training_steps_per_epoch,
        epochs=training_configuration.number_of_epochs,
        callbacks=callbacks,
        validation_data=validation_data_generator,
        validation_steps=validation_steps_per_epoch
    )

    print("Loading best model from check-point and testing...")
    # For some models, loading the model directly does not work, but loading the weights does
    # (see https://github.com/fchollet/keras/issues/4044#issuecomment-254921595)
    # best_model = keras.models.load_model(best_model_path)
    best_model = training_configuration.classifier()
    best_model.load_weights(best_model_path)

    test_data_generator.reset()
    class_labels = list(test_data_generator.class_indices.keys())
    true_classes = test_data_generator.classes
    predictions = best_model.predict_generator(test_data_generator, steps=test_steps_per_epoch)
    predicted_classes = numpy.argmax(predictions, axis=1)

    report = metrics.classification_report(true_classes, predicted_classes, target_names=class_labels)
    # accuracy = metrics.accuracy_score(true_classes, predicted_classes) # is the same as from evaluate_generator

    test_data_generator.reset()
    evaluation = best_model.evaluate_generator(test_data_generator, steps=test_steps_per_epoch)

    print(report)
    print("Total Loss: {0:.5f}".format(evaluation[0]))
    print("Total Accuracy: {0:0.5f}%".format(evaluation[1] * 100))
    print("Total Error: {0:0.5f}%".format((1 - evaluation[1]) * 100))

    end_time = time()
    print("Execution time: %.1fs" % (end_time - start_time))

    TrainingHistoryPlotter.plot_history(history,
                                        "{1}_{0}_{2:.1f}p.png".format(training_configuration.name(),
                                                                      datetime.date.today(),
                                                                      evaluation[1] * 100),
                                        show_plot=show_plot_after_training)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument("--dataset_directory", type=str, default="data",
                        help="The directory, that is used for storing the images during training")
    parser.add_argument("--model_name", type=str, default="vgg",
                        help="The model used for training the network. Currently allowed values are \'simple\' or \'vgg\'")

    parser.add_argument("--show_plot_after_training", dest="show_plot_after_training", action='store_true',
                        help="Whether to show a plot with the accuracies after training or not.")
    parser.set_defaults(show_plot_after_training=False)

    parser.add_argument("--use_existing_dataset_directory", dest="delete_and_recreate_dataset_directory",
                        action='store_false',
                        help="Whether to delete and recreate the dataset-directory (by downloading the appropriate "
                             "files from the internet, extracting and generating images) or simply use whatever data "
                             "currently is inside of that directory.")
    parser.set_defaults(delete_and_recreate_dataset_directory=True)

    parser.add_argument("-s", "--stroke_thicknesses", dest="stroke_thicknesses", default="3",
                        help="Stroke thicknesses for drawing the generated bitmaps. May define comma-separated list "
                             "of multiple stroke thicknesses, e.g. '1,2,3'")
    parser.add_argument("-offsets", "--staff_line_vertical_offsets", dest="offsets", default="",
                        help="Optional vertical offsets in pixel for drawing the symbols with superimposed "
                             "staff-lines starting at this pixel-offset from the top. Multiple offsets possible, "
                             "e.g. '81,88,95'")
    parser.add_argument("--width", default=128, type=int, help="Width of the generated images in pixel")
    parser.add_argument("--height", default=224, type=int, help="Height of the generated images in pixel")
    parser.add_argument("--minibatch_size", default=64, type=int,
                        help="Size of the minibatches for training")
    parser.add_argument("--optimizer", default="Adadelta", help="The optimizer used for the training")

    parser.add_argument("--no_dynamic_learning_rate_reduction", dest="dynamic_learning_rate_reduction",
                        action="store_false",
                        help="True, if the learning rate should be scheduled to be reduced on a plateau.")
    parser.set_defaults(dynamic_learning_rate_reduction=True)

    flags, unparsed = parser.parse_known_args()

    offsets = None
    if flags.offsets != "":
        offsets = [int(o) for o in flags.offsets.split(',')]

    train_model(flags.dataset_directory,
                flags.model_name,
                flags.show_plot_after_training,
                flags.delete_and_recreate_dataset_directory,
                [int(s) for s in flags.stroke_thicknesses.split(',')],
                flags.width,
                flags.height,
                offsets,
                flags.minibatch_size,
                flags.optimizer,
                flags.dynamic_learning_rate_reduction)
