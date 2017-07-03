from keras import Input
from keras.engine import Layer, Model
from keras.layers import Activation, BatchNormalization, Convolution2D, Dense, Flatten, MaxPooling2D, AveragePooling2D, \
    add
from keras.models import Sequential
from keras.regularizers import l2
from keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class ResNet2Configuration(TrainingConfiguration):
    """ A network with residual modules """

    def __init__(self, optimizer="Adadelta", width=96, height=192, training_minibatch_size=64):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size)

    def classifier(self) -> Sequential:
        """ Returns the classifier of this configuration """

        input = Input(shape=self.data_shape)

        layer = self.add_convolution_block_with_batch_normalization(input, 32, 7, (2, 2), 1)
        layer = MaxPooling2D()(layer)

        for i in range(1, 3):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 32, 3, is_first_convolution, 2, i)

        for i in range(1, 3):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 64, 3, is_first_convolution, 3, i)

        for i in range(1, 4):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 128, 3, is_first_convolution, 4, i)

        for i in range(1, 4):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 256, 3, is_first_convolution, 5, i)

        layer = AveragePooling2D()(layer)

        feature_vector = Flatten()(layer)

        number_of_output_classes = 32
        classification_head = Dense(units=number_of_output_classes, kernel_regularizer=l2(self.weight_decay),
                                    activation='softmax', name='output_class')(feature_vector)

        classifier = Model(inputs=[input], outputs=[classification_head])
        classifier.compile(self.get_optimizer(),
                           loss={'output_class': 'categorical_crossentropy'},
                           metrics=["accuracy"])
        return classifier

    def add_convolution_block_with_batch_normalization(self, previous_layer: Layer, filters, kernel_size,
                                                       strides, layer_number: int) -> Layer:
        layer = Convolution2D(filters, kernel_size, strides=strides, padding='same',
                              kernel_regularizer=l2(self.weight_decay), name='conv' + str(layer_number))(previous_layer)
        layer = BatchNormalization()(layer)
        layer = Activation('relu')(layer)
        return layer

    def add_res_net_block(self, previous_layer: Layer, filters, kernel_size, is_first_convolution, layer_number: int,
                          block_number: int):
        first_strides = (1, 1)
        if is_first_convolution:
            first_strides = (2, 2)  # use strides instead of max-pooling to downsample image

        layer = Convolution2D(filters, kernel_size, strides=first_strides, padding='same',
                              kernel_regularizer=l2(self.weight_decay),
                              name="conv{0}_{1}_a".format(layer_number, block_number))(
            previous_layer)
        layer = BatchNormalization()(layer)
        layer = Activation('relu')(layer)
        layer = Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(self.weight_decay),
                              name="conv{0}_{1}_b".format(layer_number, block_number))(layer)
        layer = BatchNormalization()(layer)
        layer = Activation('relu')(layer)

        shortcut = previous_layer
        if is_first_convolution:
            shortcut = Convolution2D(filters, 1, strides=first_strides, padding='same',
                                     kernel_regularizer=l2(self.weight_decay),
                                     name="conv{0}_{1}_shortcut".format(layer_number, block_number))(previous_layer)

        return add([layer, shortcut])

    def name(self) -> str:
        """ Returns the name of this configuration """
        return "res_net_2"

    def performs_localization(self) -> bool:
        return False


if __name__ == "__main__":
    configuration = ResNet2Configuration()
    classifier = configuration.classifier()
    classifier.summary()
    plot_model(classifier, to_file="res_net.png")
    print(configuration.summary())
