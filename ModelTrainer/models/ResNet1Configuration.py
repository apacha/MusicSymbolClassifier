from tensorflow.keras import Input
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer, Activation, BatchNormalization, Convolution2D, Dense, Flatten, MaxPooling2D, AveragePooling2D, \
    add
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class ResNet1Configuration(TrainingConfiguration):
    """ A network with residual modules """

    def __init__(self, optimizer: str, width: int, height: int, training_minibatch_size: int, number_of_classes: int):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size, number_of_classes=number_of_classes)

    def classifier(self) -> Sequential:
        """ Returns the model of this configuration """

        input = Input(shape=self.data_shape)

        layer = self.add_convolution_block_with_batch_normalization(input, 64, 7, (2, 2), 1)
        layer = MaxPooling2D()(layer)

        for i in range(1, 4):
            layer = self.add_res_net_block(layer, 64, 3, False, 2, i)

        for i in range(1, 4):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 128, 3, is_first_convolution, 3, i)

        for i in range(1, 4):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 256, 3, is_first_convolution, 4, i)

        for i in range(1, 4):
            is_first_convolution = i == 1
            layer = self.add_res_net_block(layer, 512, 3, is_first_convolution, 5, i)

        layer = AveragePooling2D()(layer)

        feature_vector = Flatten()(layer)

        number_of_output_classes = self.number_of_classes
        classification_head = Dense(units=number_of_output_classes, kernel_regularizer=l2(self.weight_decay),
                                    activation='softmax', name='output_class')(feature_vector)

        model = Model(inputs=[input], outputs=[classification_head])
        model.compile(self.get_optimizer(),
                      loss={'output_class': 'categorical_crossentropy'},
                      metrics=["accuracy"])
        return model

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
        return "res_net_1"

    def performs_localization(self) -> bool:
        return False


if __name__ == "__main__":
    configuration = ResNet1Configuration("Adadelta", 96, 96, 16, 32)
    configuration.classifier().summary()
    plot_model(configuration.classifier(), to_file="res_net_1.png")
    print(configuration.summary())
