from tensorflow.keras.layers import Activation, BatchNormalization, Convolution2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class VggConfiguration(TrainingConfiguration):
    """ A rudimentary configuration for starting """

    def __init__(self, optimizer: str, width: int, height: int, training_minibatch_size: int, number_of_classes: int):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size, number_of_classes=number_of_classes)

    def classifier(self) -> Sequential:
        """ Returns the model of this configuration """
        model = Sequential()

        self.add_convolution(model, 16, 3, self.weight_decay, input_shape=self.data_shape)
        self.add_convolution(model, 16, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 32, 3, self.weight_decay)
        self.add_convolution(model, 32, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 64, 3, self.weight_decay)
        self.add_convolution(model, 64, 3, self.weight_decay)
        self.add_convolution(model, 64, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 128, 3, self.weight_decay)
        self.add_convolution(model, 128, 3, self.weight_decay)
        self.add_convolution(model, 128, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 192, 3, self.weight_decay)
        self.add_convolution(model, 192, 3, self.weight_decay)
        self.add_convolution(model, 192, 3, self.weight_decay)
        self.add_convolution(model, 192, 3, self.weight_decay)
        model.add(MaxPooling2D())

        model.add(Flatten())  # Flatten
        # model.add(Dropout(0.5))
        model.add(
            Dense(units=self.number_of_classes, kernel_regularizer=l2(self.weight_decay), activation='softmax',
                  name='output_class'))

        model.compile(self.get_optimizer(), loss="categorical_crossentropy", metrics=["accuracy"])
        return model

    def add_convolution(self, model, filters, kernel_size, weight_decay, strides=(1, 1), input_shape=None):
        if input_shape is None:
            model.add(Convolution2D(filters, kernel_size, strides=strides, padding='same',
                                    kernel_regularizer=l2(weight_decay)))
        else:
            model.add(
                Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(weight_decay),
                              input_shape=input_shape))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

    def name(self) -> str:
        """ Returns the name of this configuration """
        return "vgg"

    def performs_localization(self) -> bool:
        return False


if __name__ == "__main__":
    configuration = VggConfiguration("Adadelta", 96, 96, 16, 32)
    classifier = configuration.classifier()
    classifier.summary()
    plot_model(classifier, to_file="vgg.png")
    print(configuration.summary())
