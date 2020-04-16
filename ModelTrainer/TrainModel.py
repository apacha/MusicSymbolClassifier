import argparse
import datetime
import fnmatch
import os
import pickle
from time import time
from typing import List

import tensorflow.keras
import numpy
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from ClassWeightCalculator import ClassWeightCalculator
from reporting import TelegramNotifier, GoogleSpreadsheetReporter, sklearn_reporting
from reporting.TrainingHistoryPlotter import TrainingHistoryPlotter
from datasets.TrainingDatasetProvider import TrainingDatasetProvider
from datasets.DirectoryIteratorWithBoundingBoxes import DirectoryIteratorWithBoundingBoxes
from models.ConfigurationFactory import ConfigurationFactory


def train_model(dataset_directory: str, model_name: str, stroke_thicknesses: List[int],
                width: int, height: int,
                staff_line_vertical_offsets: List[int], training_minibatch_size: int,
                optimizer: str, dynamic_learning_rate_reduction: bool, use_fixed_canvas: bool, datasets: List[str],
                class_weights_balancing_method: str,
                send_telegram_messages: bool):
    image_dataset_directory = os.path.join(dataset_directory, "images")

    bounding_boxes = None
    bounding_boxes_cache = os.path.join(dataset_directory, "bounding_boxes.txt")

    print("Loading configuration and data-readers...")
    start_time = time()

    number_of_classes = len(os.listdir(os.path.join(image_dataset_directory, "training")))
    training_configuration = ConfigurationFactory.get_configuration_by_name(model_name, optimizer, width, height,
                                                                            training_minibatch_size, number_of_classes)
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

    start_of_training = datetime.date.today()

    monitor_variable = 'val_accuracy'
    if training_configuration.performs_localization():
        monitor_variable = 'val_output_class_accuracy'

    best_model_basename = "{0}_{1}".format(start_of_training, training_configuration.name())
    best_model_path = best_model_basename + "-{epoch:02d}.h5"
    model_checkpoint = ModelCheckpoint(best_model_path, monitor=monitor_variable, save_best_only=True, verbose=1,
             save_freq='epoch')
    early_stop = EarlyStopping(monitor=monitor_variable,
                               patience=training_configuration.number_of_epochs_before_early_stopping,
                               verbose=1)
    learning_rate_reduction = ReduceLROnPlateau(monitor=monitor_variable,
                                                patience=training_configuration.number_of_epochs_before_reducing_learning_rate,
                                                verbose=1,
                                                factor=training_configuration.learning_rate_reduction_factor,
                                                min_lr=training_configuration.minimum_learning_rate)
    tensorboard_callback = TensorBoard(
            log_dir="./logs/{0}_{1}/".format(start_of_training, training_configuration.name()))
    if dynamic_learning_rate_reduction:
        callbacks = [model_checkpoint, early_stop, tensorboard_callback, learning_rate_reduction]
    else:
        print("Learning-rate reduction on Plateau disabled")
        callbacks = [model_checkpoint, early_stop, tensorboard_callback]

    class_weight_calculator = ClassWeightCalculator()
    class_weights = class_weight_calculator.calculate_class_weights(image_dataset_directory,
                                                                    method=class_weights_balancing_method,
                                                                    class_indices=training_data_generator.class_indices)
    if class_weights_balancing_method is not None:
        print("Using {0} method for obtaining class weights to compensate for an unbalanced dataset.".format(
            class_weights_balancing_method))

    print("Training on dataset...")
    history = model.fit_generator(
        generator=training_data_generator,
        steps_per_epoch=training_steps_per_epoch,
        epochs=training_configuration.number_of_epochs,
        callbacks=callbacks,
        validation_data=validation_data_generator,
        validation_steps=validation_steps_per_epoch,
        class_weight=class_weights
    )

    print("Loading latest model from check-point and testing...")
    latest_mtime = 0
    latest_file = None
    for f in os.listdir('.'):
        if fnmatch.fnmatch(f, '*.h5'):
            fd = os.open(f, os.O_RDONLY)
            st = os.fstat(fd)
            mt = st.st_mtime
            if not latest_file or mt > latest_mtime:
                latest_mtime = mt
                latest_file = f

    print('latest model file is {0}'.format(latest_file))
    best_model = tensorflow.keras.models.load_model(latest_file)

    test_data_generator.reset()
    file_names = test_data_generator.filenames
    class_labels = os.listdir(os.path.join(image_dataset_directory, "test"))
    # Notice that some classes have so few elements, that they are not present in the test-set and do not
    # appear in the final report. To obtain the correct classes, we have to enumerate all non-empty class
    # directories inside the test-folder and use them as labels
    names_of_classes_with_test_data = [
        class_name for class_name in class_labels
        if os.listdir(os.path.join(image_dataset_directory, "test", class_name))]
    true_classes = test_data_generator.classes
    predictions = best_model.predict_generator(test_data_generator, steps=test_steps_per_epoch)
    if training_configuration.performs_localization():
        predicted_classes = numpy.argmax(predictions[0], axis=1)
    else:
        predicted_classes = numpy.argmax(predictions, axis=1)

    test_data_generator.reset()
    evaluation = best_model.evaluate_generator(test_data_generator, steps=test_steps_per_epoch)
    classification_accuracy = 0

    print("Reporting classification statistics with micro average")
    report = sklearn_reporting.classification_report(true_classes, predicted_classes, digits=3,
                                                     target_names=names_of_classes_with_test_data, average='micro')
    print(report)

    print("Reporting classification statistics with macro average")
    report = sklearn_reporting.classification_report(true_classes, predicted_classes, digits=3,
                                                     target_names=names_of_classes_with_test_data, average='macro')
    print(report)

    print("Reporting classification statistics with weighted average")
    report = sklearn_reporting.classification_report(true_classes, predicted_classes, digits=3,
                                                     target_names=names_of_classes_with_test_data, average='weighted'
                                                     )
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
    execution_time_in_seconds = round(end_time - start_time)
    print("Execution time: {0:.1f}s".format(end_time - start_time))

    training_result_image = "{1}_{0}_{2:.1f}p.png".format(training_configuration.name(), start_of_training,
                                                          classification_accuracy * 100)
    TrainingHistoryPlotter.plot_history(history, training_result_image)

    datasets_string = str.join(",", datasets)
    notification_message = "Training on {0} dataset with model {1} finished. " \
                           "Accuracy: {2:0.5f}%".format(datasets_string, model_name, classification_accuracy * 100)
    if send_telegram_messages:
        TelegramNotifier.send_message_via_telegram(notification_message, training_result_image)
    else:
        print(notification_message)

    dataset_size = training_data_generator.samples + validation_data_generator.samples + test_data_generator.samples
    stroke_thicknesses_string = ",".join(map(str, stroke_thicknesses))
    staff_line_vertical_offsets_string = ",".join(map(str, staff_line_vertical_offsets))
    image_sizes = "{0}x{1}px".format(training_configuration.input_image_rows,
                                     training_configuration.input_image_columns)
    data_augmentation = "{0}% zoom, {1}° rotation".format(int(training_configuration.zoom_range * 100),
                                                          training_configuration.rotation_range)
    today = "{0:02d}.{1:02d}.{2}".format(start_of_training.day, start_of_training.month, start_of_training.year)
    balancing_method = "None" if class_weights_balancing_method is None else class_weights_balancing_method

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
                                                           use_fixed_canvas=use_fixed_canvas,
                                                           datasets=datasets_string,
                                                           execution_time_in_seconds=execution_time_in_seconds,
                                                           balancing_method=balancing_method)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument("--dataset_directory", type=str, default="data",
                        help="The directory, that is used for storing the images during training")
    parser.add_argument("--model_name", type=str, default="res_net_4",
                        help="The model used for training the network. Run ListAvailableConfigurations.ps1 or "
                             "models/ConfigurationFactory.py to get a list of all available configurations")

    parser.add_argument("--use_existing_dataset_directory", dest="delete_and_recreate_dataset_directory",
                        action='store_false',
                        help="Whether to delete and recreate the dataset-directory (by downloading the appropriate "
                             "files from the internet, extracting and generating images) or simply use whatever data "
                             "currently is inside of that directory.")
    parser.set_defaults(delete_and_recreate_dataset_directory=True)

    parser.add_argument("--minibatch_size", default=16, type=int,
                        help="Size of the minibatches for training, typically one of 8, 16, 32, 64 or 128")
    parser.add_argument("--optimizer", default="Adadelta", type=str,
                        help="The optimizer used for the training, can be SGD, Adam or Adadelta")

    parser.add_argument("--no_dynamic_learning_rate_reduction", dest="dynamic_learning_rate_reduction",
                        action="store_false",
                        help="True, if the learning rate should not be scheduled to be reduced on a plateau.")
    parser.set_defaults(dynamic_learning_rate_reduction=True)
    parser.add_argument("--class_weights_balancing_method", default=None, type=str,
                        help="The optional weight balancing method for handling unbalanced datasets. If provided,"
                             "valid choices are simple or skBalance. 'simple' uses 1/sqrt(#samples_per_class) as "
                             "weights for samples from each class to compensate for classes that are underrepresented."
                             "'skBalance' uses the Python SkLearn module to calculate more sophisticated weights.")
    parser.add_argument("--no_telegram_messages", dest="send_telegram_messages", action="store_false",
                        help="Send messages via telegram")
    parser.set_defaults(send_telegram_messages=True)


    TrainingDatasetProvider.add_arguments_for_training_dataset_provider(parser)

    flags, unparsed = parser.parse_known_args()

    offsets = []
    if flags.offsets != "":
        offsets = [int(o) for o in flags.offsets.split(',')]
    stroke_thicknesses_for_generated_symbols = [int(s) for s in flags.stroke_thicknesses.split(',')]

    if flags.datasets == "":
        raise Exception("No dataset selected. Specify the dataset for the training via the --dataset parameter")
    datasets = flags.datasets.split(',')

    if flags.delete_and_recreate_dataset_directory:
        training_dataset_provider = TrainingDatasetProvider(flags.dataset_directory)
        training_dataset_provider.recreate_and_prepare_datasets_for_training(
            datasets=datasets, width=flags.width,
            height=flags.height,
            use_fixed_canvas=flags.use_fixed_canvas,
            stroke_thicknesses_for_generated_symbols=stroke_thicknesses_for_generated_symbols,
            staff_line_spacing=flags.staff_line_spacing,
            staff_line_vertical_offsets=offsets,
            random_position_on_canvas=flags.random_position_on_canvas)
        training_dataset_provider.resize_all_images_to_fixed_size(flags.width, flags.height)
        training_dataset_provider.split_dataset_into_training_validation_and_test_set()

    train_model(dataset_directory=flags.dataset_directory,
                model_name=flags.model_name,
                stroke_thicknesses=stroke_thicknesses_for_generated_symbols,
                width=flags.width,
                height=flags.height,
                staff_line_vertical_offsets=offsets,
                training_minibatch_size=flags.minibatch_size,
                optimizer=flags.optimizer,
                dynamic_learning_rate_reduction=flags.dynamic_learning_rate_reduction,
                use_fixed_canvas=flags.use_fixed_canvas,
                datasets=datasets,
                class_weights_balancing_method=flags.class_weights_balancing_method,
                flags.send_telegram_messages)

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
