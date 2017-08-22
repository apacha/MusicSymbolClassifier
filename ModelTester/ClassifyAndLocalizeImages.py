#!/usr/bin/python
import sys
from argparse import ArgumentParser
from typing import List

import keras
import numpy
from PIL import ImageDraw, Image
from scipy import ndimage
from scipy.misc import imresize
import os


def test_model(model_path: str, image_paths: List[str]):
    # model_path = "C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\results\\2017-06-05_vgg4.h5"
    # model_name = "vgg4"
    # image_path = "C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\Quarter1.png"

    print("Weights loaded from : ", model_path)

    print("Loading classifier...")
    classifier = keras.models.load_model(model_path)
    classifier.summary()

    input_shape = classifier.input_shape[1:4]  # For some reason, input-shape has the form (None, 1, 2, 3)
    print(" Input shape: {0}, Output: {1} classes".format(input_shape, classifier.output_shape[1]))

    for image_path in image_paths:
        input_image = ndimage.imread(image_path, mode="RGB")
        print("\nLoading image {0} of shape {1}".format(image_path, input_image.shape))

        # print("Preprocessing image ...")
        # print("  Resizing to 224x128x3")
        # normalized_input_image = imresize(input_image, size=(192, 96, 3))
        # normalized_input_image = normalized_input_image.astype(numpy.float32)
        # input_image = normalized_input_image
        #
        # print(" Result: shape: {0}, dtype: {1}, mean: {2:.3f}, std: {3:.3f}".format(normalized_input_image.shape,
        #                                                                             normalized_input_image.dtype,
        #                                                                             numpy.mean(normalized_input_image),
        #                                                                             numpy.std(normalized_input_image)))
        #
        # Image.fromarray(normalized_input_image.astype(numpy.uint8), mode="RGB").save("normalized_input.png")


        # plot_model(classifier, to_file='classifier.png')

        print("Classifying image ...")
        # print("1/1 [==============================] - 0s")

        result = classifier.predict(numpy.array([input_image]))
        scores = result[0].flatten()
        bounding_box = result[1].flatten()
        print("Bounding-Box: {0}".format(bounding_box))
        class_with_highest_probability = numpy.where(scores == scores.max())[0][0]

        # Follows the order of the directories as listed by python command
        # os.listdir("C:/Users/Alex/Repositories/MusicSymbolClassifier/HomusTrainer/data/images")
        class_names = ['12-8-Time',
                       '2-2-Time',
                       '2-4-Time',
                       '3-4-Time',
                       '3-8-Time',
                       '4-4-Time',
                       '6-8-Time',
                       '9-8-Time',
                       'Barline',
                       'C-Clef',
                       'Common-Time',
                       'Cut-Time',
                       'Dot',
                       'Double-Sharp',
                       'Eighth-Note',
                       'Eighth-Rest',
                       'F-Clef',
                       'Flat',
                       'G-Clef',
                       'Half-Note',
                       'Natural',
                       'Quarter-Note',
                       'Quarter-Rest',
                       'Sharp',
                       'Sixteenth-Note',
                       'Sixteenth-Rest',
                       'Sixty-Four-Note',
                       'Sixty-Four-Rest',
                       'Thirty-Two-Note',
                       'Thirty-Two-Rest',
                       'Whole-Half-Rest',
                       'Whole-Note']

        if len(image_paths) == 1:
            print("Class scores:")
            for i in range(len(scores)):
                print("{0:<18s} {1:.5f}".format(class_names[i], scores[i]))

        most_likely_class = class_names[class_with_highest_probability]
        print(" Image is most likely: {0} (certainty: {1:0.2f})".format(most_likely_class,
                                                                        scores[class_with_highest_probability]))

        red = (255, 0, 0)
        image_with_bounding_box = Image.fromarray(input_image)
        draw = ImageDraw.Draw(image_with_bounding_box)
        rectangle = (bounding_box[0], bounding_box[1], bounding_box[0] + bounding_box[2],
                     bounding_box[1] + bounding_box[3])
        draw.rectangle(rectangle, fill=None, outline=red)
        path = os.path.dirname(image_path)
        file_name, extension = os.path.splitext(os.path.basename(image_path))
        image_with_bounding_box.save(
            os.path.join(path, "{0}_{1}_localization{2}".format(file_name, most_likely_class, extension)))


if __name__ == "__main__":
    parser = ArgumentParser("Classify an RGB-image with a pre-trained classifier")
    parser.add_argument("-c", "--classifier", dest="model_path",
                        help="path to the classifier that contains the weights (*.h5)",
                        default="2017-08-17_vgg4_with_localization.h5")
    parser.add_argument("-i", "--images", dest="image_paths", nargs="+",
                        help="path(s) to the rgb image(s) to classify",
                        # default="C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\ModelTrainer\\data\\images\\3-4-Time\\1-13_3.png abc",
                        default=""
                        )
    parser.add_argument("-d", "--image_directory", dest="image_directory",
                        help="path to a folder that contains all images that should be classified",
                        # default="C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\ModelTester\\test-data\\",
                        default=""
                        )

    args = parser.parse_args()

    if len(args.image_paths) == 0 and len(args.image_directory) == 0:
        print("No data for classification provided. Aborting")
        parser.print_help()
        sys.exit(-1)

    files = []

    if len(args.image_paths) > 0:
        if type(args.image_paths) == str:
            files.append(args.image_paths)
        else:
            files += args.image_paths

    if len(args.image_directory) > 0:
        files_in_directory = os.listdir(args.image_directory)
        images_in_directory = [os.path.join(args.image_directory, i) for i in files_in_directory if
                               i.endswith("png") or i.endswith("jpg")]
        files += images_in_directory

    test_model(args.model_path, files)
