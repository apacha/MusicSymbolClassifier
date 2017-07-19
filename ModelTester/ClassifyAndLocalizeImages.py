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

from models.ConfigurationFactory import ConfigurationFactory


def test_model(model_path: str, model_name: str, image_paths: List[str]):
    # model_path = "C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\results\\2017-06-05_vgg4.h5"
    # model_name = "vgg4"
    # image_path = "C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\Quarter1.png"

    print("Model: ", model_name)
    print("Weights loaded from : ", model_path)

    print("Loading classifier...")
    # best_model = ConfigurationFactory().get_configuration_by_name(model_name).classifier()
    # best_model.load_weights(model_path)
    # classifier = best_model
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

        print("Class scores:")

        for i in range(len(scores)):
            print("{0:<18s} {1:.5f}".format(class_names[i], scores[i]))

        print(" Image is most likely: {0} (certainty: {1:0.2f})".format(class_names[class_with_highest_probability],
                                                                        scores[class_with_highest_probability]))

        red = (255, 0, 0)
        image_with_bounding_box = Image.fromarray(input_image)
        draw = ImageDraw.Draw(image_with_bounding_box)
        rectangle = (bounding_box[0], bounding_box[1], bounding_box[0] + bounding_box[2],
                     bounding_box[1] + bounding_box[3])
        draw.rectangle(rectangle, fill=None, outline=red)
        path = os.path.dirname(image_path)
        file_name, extension = os.path.splitext(os.path.basename(image_path))
        image_with_bounding_box.save(os.path.join(path, file_name + "_localization" + extension))


if __name__ == "__main__":
    parser = ArgumentParser("Classify an RGB-image with a pre-trained classifier")
    parser.add_argument("-c", "--classifier", dest="model_path",
                        help="path to the classifier that contains the weights (*.h5)",
                        default="C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\results\\2017-06-05_vgg4.h5")
    parser.add_argument("-m", "--model", dest="model_name",
                        help="name of the model being used",
                        default="vgg4")
    parser.add_argument("-i", "--images", dest="image_paths", nargs="+",
                        help="path(s) to the rgb image(s) to classify",
                        default="C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\Quarter1.png")

    args = parser.parse_args()

    if len(sys.argv) < 7:
        parser.print_help()
        sys.exit(-1)

    test_model(args.model_path, args.model_name, args.image_paths)
