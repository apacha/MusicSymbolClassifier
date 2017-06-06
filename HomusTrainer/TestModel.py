#!/usr/bin/python
import sys
from argparse import ArgumentParser

import numpy
from scipy import ndimage

from models.ConfigurationFactory import ConfigurationFactory


def test_model(model_path: str, model_name: str, image_path: str):
    # model_path = "C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\results\\2017-06-05_vgg4.h5"
    # model_name = "vgg4"
    # image_path = "C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\Quarter1.png"

    print("Model: ", model_name)
    print("Weights loaded from : ", model_path)
    print("Image: ", image_path)

    print("Loading image ...")
    input_image = ndimage.imread(image_path, mode="RGB")
    print(" Shape: {0}".format(input_image.shape))

    print("Loading classifier...")
    best_model = ConfigurationFactory().get_configuration_by_name(model_name).classifier()
    best_model.load_weights(model_path)
    classifier = best_model
    # classifier = keras.models.load_model(model_path)
    classifier.summary()

    input_shape = classifier.input_shape[1:4]  # For some reason, input-shape has the form (None, 1, 2, 3)
    print(" Input shape: {0}, Output: {1} classes".format(input_shape, classifier.output_shape[1]))

    # print("Preprocessing image ...")
    # print("  Resizing to 224x128x3")
    # normalized_input_image = resize(input_image, output_shape=(224, 128, 3), preserve_range=True)
    # normalized_input_image = normalized_input_image.astype(numpy.float32)
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

    scores = classifier.predict(numpy.array([input_image])).flatten()
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

    print ("Class scores:")

    for i in range(len(scores)):
        print("{0:<18s} {1:.5f}".format(class_names[i], scores[i]))

    print(" Image is most likely: {0} (certainty: {1:0.2f})".format(class_names[class_with_highest_probability],
                                                                    scores[class_with_highest_probability]))


if __name__ == "__main__":
    parser = ArgumentParser("Classify an RGB-image with a pre-trained classifier")
    parser.add_argument("-c", "--classifier", dest="model_path",
                        help="path to the classifier that contains the weights (*.h5)",
                        default="C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\results\\2017-06-05_vgg4.h5")
    parser.add_argument("-m", "--model", dest="model_name",
                        help="name of the model being used",
                        default="vgg4")
    parser.add_argument("-i", "--image", dest="image_path",
                        help="path to the rgb image to classify",
                        default="C:\\Users\\Alex\\Repositories\\MusicSymbolClassifier\\HomusTrainer\\Quarter1.png")

    args = parser.parse_args()

    if len(sys.argv) < 7:
        parser.print_help()
        sys.exit(-1)

    test_model(args.model_path, args.model_name, args.image_path)
