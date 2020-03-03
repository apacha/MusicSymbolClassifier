from tensorflow.keras.layers import Activation, BatchNormalization, Convolution2D, MaxPooling2D, \
    GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class Vgg4ConvOnlyConfiguration(TrainingConfiguration):
    """ A simplified VGG network that uses no fully-connected layer, but instead a Convolutional Layer + Global Average Pooling """

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

        model.add(Convolution2D(self.number_of_classes, kernel_size=(1, 1), padding='same'))
        model.add(GlobalAveragePooling2D())
        model.add(Activation('softmax', name='output_class'))

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
        return "vgg4_conv_only"

    def performs_localization(self) -> bool:
        return False


if __name__ == "__main__":
    configuration = Vgg4ConvOnlyConfiguration("Adadelta", 96, 96, 16, 32)
    configuration.classifier().summary()
    plot_model(configuration.classifier(), to_file="vgg4_conv_only.png")
    print(configuration.summary())
