from keras.layers import Activation, BatchNormalization, Convolution2D, Dense, Dropout, Flatten, MaxPooling2D, \
    AveragePooling2D
from keras.models import Sequential
from keras.optimizers import SGD, Adam
from keras.regularizers import l2
from keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class Vgg4Configuration(TrainingConfiguration):
    """ The winning VGG-Net 4 configuration from Deep Learning course """

    def __init__(self, optimizer, width, height, training_minibatch_size, number_of_classes):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size, number_of_classes=number_of_classes)

    def classifier(self) -> Sequential:
        """ Returns the model of this configuration """
        model = Sequential()

        self.add_convolution(model, 32, 3, self.weight_decay, input_shape=self.data_shape)
        self.add_convolution(model, 32, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 64, 3, self.weight_decay)
        self.add_convolution(model, 64, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 128, 3, self.weight_decay)
        self.add_convolution(model, 128, 3, self.weight_decay)
        self.add_convolution(model, 128, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 256, 3, self.weight_decay)
        self.add_convolution(model, 256, 3, self.weight_decay)
        self.add_convolution(model, 256, 3, self.weight_decay)
        model.add(MaxPooling2D())

        self.add_convolution(model, 512, 3, self.weight_decay)
        self.add_convolution(model, 512, 3, self.weight_decay)
        self.add_convolution(model, 512, 3, self.weight_decay)
        model.add(AveragePooling2D())

        model.add(Flatten())  # Flatten
        # model.add(Dropout(0.5))
        model.add(Dense(units=32, kernel_regularizer=l2(self.weight_decay), activation='softmax', name='output_class'))

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
        return "vgg4"

    def performs_localization(self) -> bool:
        return False


if __name__ == "__main__":
    configuration = Vgg4Configuration("Adadelta", 96, 96, 16, 32)
    configuration.classifier().summary()
    plot_model(configuration.classifier(), to_file="vgg4.png")
    print(configuration.summary())
