import argparse
import datetime
import os
import pickle
import shutil
from datetime import date
from time import time
from typing import List

import numpy
import numpy as np
from PIL import Image
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
from sklearn import metrics

import GoogleSpreadsheetReporter
import TelegramNotifier
from datasets.ImageResizer import ImageResizer
from TrainingHistoryPlotter import TrainingHistoryPlotter
from datasets.DatasetSplitter import DatasetSplitter
from datasets.DirectoryIteratorWithBoundingBoxes import DirectoryIteratorWithBoundingBoxes
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
                staff_line_spacing: int,
                training_minibatch_size: int,
                optimizer: str,
                dynamic_learning_rate_reduction: bool,
                use_fixed_canvas: bool):
    raw_dataset_directory = os.path.join(dataset_directory, "raw")
    image_dataset_directory = os.path.join(dataset_directory, "images")
    bounding_boxes = None
    bounding_boxes_cache = os.path.join(dataset_directory, "bounding_boxes.txt")

    if delete_and_recreate_dataset_directory:
        print("Deleting dataset directory {0}".format(dataset_directory))
        if os.path.exists(dataset_directory):
            shutil.rmtree(dataset_directory)

        dataset_downloader = HomusDatasetDownloader(raw_dataset_directory)
        dataset_downloader.download_and_extract_dataset()
        generated_image_width = width
        generated_image_height = height
        if not use_fixed_canvas:
            # If we are not using a fixed canvas, remove those arguments to allow symbols being drawn at their original shapes
            generated_image_width, generated_image_height = None, None
        bounding_boxes = HomusImageGenerator.create_images(raw_dataset_directory, image_dataset_directory,
                                                           stroke_thicknesses, generated_image_width,
                                                           generated_image_height, staff_line_spacing,
                                                           staff_line_vertical_offsets)
        with open(bounding_boxes_cache, "wb") as cache:
            pickle.dump(bounding_boxes, cache)

        image_resizer = ImageResizer()
        image_resizer.resize_all_images(image_dataset_directory, width, height, Image.LANCZOS)

        dataset_splitter = DatasetSplitter(image_dataset_directory, image_dataset_directory)
        dataset_splitter.delete_split_directories()
        dataset_splitter.split_images_into_training_validation_and_test_set()

    print("Loading configuration and data-readers...")
    start_time = time()

    training_configuration = ConfigurationFactory.get_configuration_by_name(model_name, optimizer, width, height,
                                                                            training_minibatch_size)

    if training_configuration.performs_localization() and bounding_boxes is None:
        # Try to unpickle
        with open(bounding_boxes_cache, "rb") as cache:
            bounding_boxes = pickle.load(cache)

    if not training_configuration.performs_localization():
        bounding_boxes = None

    train_generator = ImageDataGenerator(rotation_range=training_configuration.rotation_range,
                                         zoom_range=training_configuration.zoom_range
                                         )
    training_data_generator = DirectoryIteratorWithBoundingBoxes(
        directory=os.path.join(image_dataset_directory, "training"),
        image_data_generator=train_generator,
        target_size=(training_configuration.input_image_rows,
                     training_configuration.input_image_columns),
        batch_size=training_configuration.training_minibatch_size,
        bounding_boxes=bounding_boxes,
    )
    training_steps_per_epoch = np.math.ceil(training_data_generator.samples / training_data_generator.batch_size)

    validation_generator = ImageDataGenerator()
    validation_data_generator = DirectoryIteratorWithBoundingBoxes(
        directory=os.path.join(image_dataset_directory, "validation"),
        image_data_generator=validation_generator,
        target_size=(
            training_configuration.input_image_rows,
            training_configuration.input_image_columns),
        batch_size=training_configuration.training_minibatch_size,
        bounding_boxes=bounding_boxes)
    validation_steps_per_epoch = np.math.ceil(validation_data_generator.samples / validation_data_generator.batch_size)

    test_generator = ImageDataGenerator()
    test_data_generator = DirectoryIteratorWithBoundingBoxes(
        directory=os.path.join(image_dataset_directory, "test"),
        image_data_generator=test_generator,
        target_size=(training_configuration.input_image_rows,
                     training_configuration.input_image_columns),
        batch_size=training_configuration.training_minibatch_size,
        shuffle=False,
        bounding_boxes=bounding_boxes)
    test_steps_per_epoch = np.math.ceil(test_data_generator.samples / test_data_generator.batch_size)

    model = training_configuration.classifier()
    model.summary()

    print("Model {0} loaded.".format(training_configuration.name()))
    print(training_configuration.summary())

    best_model_path = "{1}_{0}.h5".format(training_configuration.name(), datetime.date.today())

    monitor_variable = 'val_acc'
    if training_configuration.performs_localization():
        monitor_variable = 'val_output_class_acc'

    model_checkpoint = ModelCheckpoint(best_model_path, monitor=monitor_variable, save_best_only=True, verbose=1)
    early_stop = EarlyStopping(monitor=monitor_variable,
                               patience=training_configuration.number_of_epochs_before_early_stopping,
                               verbose=1)
    learning_rate_reduction = ReduceLROnPlateau(monitor=monitor_variable,
                                                patience=training_configuration.number_of_epochs_before_reducing_learning_rate,
                                                verbose=1,
                                                factor=training_configuration.learning_rate_reduction_factor,
                                                min_lr=training_configuration.minimum_learning_rate)
    if dynamic_learning_rate_reduction:
        callbacks = [model_checkpoint, early_stop, learning_rate_reduction]
    else:
        print("Learning-rate reduction on Plateau disabled")
        callbacks = [model_checkpoint, early_stop]

    print("Training on dataset...")
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
    file_names = test_data_generator.filenames
    class_labels = list(test_data_generator.class_indices.keys())
    class_labels.sort()
    true_classes = test_data_generator.classes
    predictions = best_model.predict_generator(test_data_generator, steps=test_steps_per_epoch)
    if training_configuration.performs_localization():
        predicted_classes = numpy.argmax(predictions[0], axis=1)
    else:
        predicted_classes = numpy.argmax(predictions, axis=1)

    report = metrics.classification_report(true_classes, predicted_classes, target_names=class_labels)

    test_data_generator.reset()
    evaluation = best_model.evaluate_generator(test_data_generator, steps=test_steps_per_epoch)
    classification_accuracy = 0

    print(report)

    indices_of_misclassified_files = [i for i, e in enumerate(true_classes - predicted_classes) if e != 0]
    misclassified_files = [file_names[i] for i in indices_of_misclassified_files]
    misclassified_files_actual_prediction_indices = [predicted_classes[i] for i in indices_of_misclassified_files]
    misclassified_files_actual_prediction_classes = [class_labels[i] for i in
                                                     misclassified_files_actual_prediction_indices]
    print("Misclassified files:")
    for i in range(len(misclassified_files)):
        print("\t{0} is incorrectly classified as {1}".format(misclassified_files[i],
                                                              misclassified_files_actual_prediction_classes[i]))

    for i in range(len(best_model.metrics_names)):
        current_metric = best_model.metrics_names[i]
        print("{0}: {1:.5f}".format(current_metric, evaluation[i]))
        if current_metric == 'acc' or current_metric == 'output_class_acc':
            classification_accuracy = evaluation[i]
    print("Total Accuracy: {0:0.5f}%".format(classification_accuracy * 100))
    print("Total Error: {0:0.5f}%".format((1 - classification_accuracy) * 100))

    end_time = time()
    print("Execution time: %.1fs" % (end_time - start_time))

    training_result_image = "{1}_{0}_{2:.1f}p.png".format(training_configuration.name(), datetime.date.today(),
                                                          classification_accuracy * 100)
    TrainingHistoryPlotter.plot_history(history, training_result_image, show_plot=show_plot_after_training)

    notification_message = "Training on HOMUS dataset with model {0} finished. " \
                           "Accuracy: {1:0.5f}%".format(model_name, classification_accuracy * 100)
    TelegramNotifier.send_message_via_telegram(notification_message, training_result_image)

    dataset_size = training_data_generator.samples + validation_data_generator.samples + test_data_generator.samples
    stroke_thicknesses_string = ",".join(map(str, stroke_thicknesses))
    staff_line_vertical_offsets_string = ",".join(map(str, staff_line_vertical_offsets))
    image_sizes = "{0}x{1}px".format(training_configuration.input_image_rows,
                                     training_configuration.input_image_columns)
    data_augmentation = "{0}% zoom, {1}° rotation".format(int(training_configuration.zoom_range * 100),
                                                          training_configuration.rotation_range)
    today = "{0:02d}.{1:02d}.{2}".format(date.today().day, date.today().month, date.today().year)
    GoogleSpreadsheetReporter.append_result_to_spreadsheet(dataset_size=dataset_size, image_sizes=image_sizes,
                                                           stroke_thicknesses=stroke_thicknesses_string,
                                                           staff_lines=staff_line_vertical_offsets_string,
                                                           model_name=model_name, data_augmentation=data_augmentation,
                                                           optimizer=optimizer,
                                                           early_stopping=training_configuration.number_of_epochs_before_early_stopping,
                                                           reduction_patience=training_configuration.number_of_epochs_before_reducing_learning_rate,
                                                           learning_rate_reduction_factor=training_configuration.learning_rate_reduction_factor,
                                                           minibatch_size=training_minibatch_size,
                                                           initialization=training_configuration.initialization,
                                                           initial_learning_rate=training_configuration.get_initial_learning_rate(),
                                                           accuracy=classification_accuracy,
                                                           date=today,
                                                           use_fixed_canvas=use_fixed_canvas)


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

    parser.add_argument("--staff_line_spacing", default="14", type=int, help="Spacing between two staff-lines in pixel")
    parser.add_argument("-offsets", "--staff_line_vertical_offsets", dest="offsets", default="",
                        help="Optional vertical offsets in pixel for drawing the symbols with superimposed "
                             "staff-lines starting at this pixel-offset from the top. Multiple offsets possible, "
                             "e.g. '81,88,95'")
    parser.add_argument("--width", default=96, type=int, help="Width of the input-images for the network in pixel")
    parser.add_argument("--height", default=192, type=int, help="Height of the input-images for the network in pixel")
    parser.add_argument("--minibatch_size", default=64, type=int,
                        help="Size of the minibatches for training, typically one of 8, 16, 32, 64 or 128")
    parser.add_argument("--optimizer", default="Adadelta",
                        help="The optimizer used for the training, can be SGD, Adam or Adadelta")

    parser.add_argument("--no_dynamic_learning_rate_reduction", dest="dynamic_learning_rate_reduction",
                        action="store_false",
                        help="True, if the learning rate should not be scheduled to be reduced on a plateau.")
    parser.set_defaults(dynamic_learning_rate_reduction=True)

    parser.add_argument("--disable_fixed_canvas_size", dest="use_fixed_canvas",
                        action="store_false",
                        help="True, if the images should be drawn on a fixed canvas with the specified width and height."
                             "False to draw the symbols with their original sizes (each symbol might be different)")
    parser.set_defaults(use_fixed_canvas=True)

    flags, unparsed = parser.parse_known_args()

    offsets = []
    if flags.offsets != "":
        offsets = [int(o) for o in flags.offsets.split(',')]

    train_model(dataset_directory=flags.dataset_directory,
                model_name=flags.model_name,
                show_plot_after_training=flags.show_plot_after_training,
                delete_and_recreate_dataset_directory=flags.delete_and_recreate_dataset_directory,
                stroke_thicknesses=[int(s) for s in flags.stroke_thicknesses.split(',')],
                width=flags.width,
                height=flags.height,
                staff_line_vertical_offsets=offsets,
                staff_line_spacing=flags.staff_line_spacing,
                training_minibatch_size=flags.minibatch_size,
                optimizer=flags.optimizer,
                dynamic_learning_rate_reduction=flags.dynamic_learning_rate_reduction,
                use_fixed_canvas=flags.use_fixed_canvas)

    # To run in in python console
    # dataset_directory = 'data'
    # model_name = 'res_net_3_small'
    # delete_and_recreate_dataset_directory = True
    # stroke_thicknesses = [3]
    # width = 96
    # height = 192
    # staff_line_vertical_offsets = None
    # staff_line_spacing = 14
    # training_minibatch_size = 32
    # optimizer = 'Adadelta'
    # dynamic_learning_rate_reduction = True
