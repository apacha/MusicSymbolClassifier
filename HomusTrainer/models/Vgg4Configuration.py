from keras.layers import Activation, BatchNormalization, Convolution2D, Dense, Dropout, Flatten, MaxPooling2D, \
    AveragePooling2D
from keras.models import Sequential
from keras.optimizers import SGD, Adam
from keras.regularizers import l2

from models.TrainingConfiguration import TrainingConfiguration


class Vgg4Configuration(TrainingConfiguration):
    """ The winning VGG-Net 4 configuration from Deep Learning course """

    def __init__(self, optimizer="Adadelta", width=128, height=224, training_minibatch_size=64):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size)

    def classifier(self) -> Sequential:
        """ Returns the classifier of this configuration """
        classifier = Sequential()

        self.add_convolution(classifier, 32, 3, self.weight_decay, input_shape=self.data_shape)
        self.add_convolution(classifier, 32, 3, self.weight_decay)
        classifier.add(MaxPooling2D())

        self.add_convolution(classifier, 64, 3, self.weight_decay)
        self.add_convolution(classifier, 64, 3, self.weight_decay)
        classifier.add(MaxPooling2D())

        self.add_convolution(classifier, 128, 3, self.weight_decay)
        self.add_convolution(classifier, 128, 3, self.weight_decay)
        self.add_convolution(classifier, 128, 3, self.weight_decay)
        classifier.add(MaxPooling2D())

        self.add_convolution(classifier, 256, 3, self.weight_decay)
        self.add_convolution(classifier, 256, 3, self.weight_decay)
        self.add_convolution(classifier, 256, 3, self.weight_decay)
        classifier.add(MaxPooling2D())

        self.add_convolution(classifier, 512, 3, self.weight_decay)
        self.add_convolution(classifier, 512, 3, self.weight_decay)
        self.add_convolution(classifier, 512, 3, self.weight_decay)
        classifier.add(AveragePooling2D())

        classifier.add(Flatten())  # Flatten
        # classifier.add(Dropout(0.5))
        classifier.add(Dense(units=32, kernel_regularizer=l2(self.weight_decay)))
        classifier.add(Activation('softmax', name="output_node"))

        classifier.compile(self.get_optimizer(), loss="categorical_crossentropy", metrics=["accuracy"])
        return classifier

    def add_convolution(self, classifier, filters, kernel_size, weight_decay, strides=(1, 1), input_shape=None):
        if input_shape is None:
            classifier.add(Convolution2D(filters, kernel_size, strides=strides, padding='same',
                                         kernel_regularizer=l2(weight_decay)))
        else:
            classifier.add(
                Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(weight_decay),
                              input_shape=input_shape))
        classifier.add(BatchNormalization())
        classifier.add(Activation('relu'))

    def name(self) -> str:
        """ Returns the name of this configuration """
        return "vgg4"
