from keras.layers import Activation, BatchNormalization, Convolution2D, Dense, Dropout, Flatten, MaxPooling2D, \
    AveragePooling2D
from keras.models import Sequential
from keras.optimizers import SGD
from keras.regularizers import l2

from models.TrainingConfiguration import TrainingConfiguration


class Vgg4Configuration(TrainingConfiguration):
    """ The winning VGG-Net 4 configuration from Deep Learning course """

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
        #classifier.add(Dropout(0.5))
        classifier.add(Dense(units=32, kernel_regularizer=l2(self.weight_decay)))
        classifier.add(Activation('softmax', name="output_node"))

        stochastic_gradient_descent = SGD(lr=self.learning_rate, momentum=self.nesterov_momentum, nesterov=True)
        classifier.compile(stochastic_gradient_descent, loss="categorical_crossentropy", metrics=["accuracy"])
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
