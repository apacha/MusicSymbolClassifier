from tensorflow.keras import Input
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer, Activation, BatchNormalization, Convolution2D, Dense, Flatten, MaxPooling2D, AveragePooling2D, \
    add
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class ResNet3SmallWithLocalization(TrainingConfiguration):
    """ A network with residual modules """

    def __init__(self, optimizer: str, width: int, height: int, training_minibatch_size: int, number_of_classes: int):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size, number_of_classes=number_of_classes)

    def classifier(self) -> Sequential:
        """ Returns the model of this configuration """

        input = Input(shape=self.data_shape)

        layer = self.add_convolution(input, 16, 3)
        layer = self.add_res_net_block(layer, 16, 3, False)
        layer = MaxPooling2D()(layer)

        layer = self.add_res_net_block(layer, 32, 3, True)
        layer = self.add_res_net_block(layer, 32, 3, False)
        layer = MaxPooling2D()(layer)

        layer = self.add_res_net_block(layer, 64, 3, True)
        layer = self.add_res_net_block(layer, 64, 3, False)
        layer = self.add_res_net_block(layer, 64, 3, False)
        layer = MaxPooling2D()(layer)

        layer = self.add_res_net_block(layer, 128, 3, True)
        layer = self.add_res_net_block(layer, 128, 3, False)
        layer = self.add_res_net_block(layer, 128, 3, False)
        layer = MaxPooling2D()(layer)

        layer = self.add_res_net_block(layer, 256, 3, True)
        layer = self.add_res_net_block(layer, 256, 3, False)
        layer = self.add_res_net_block(layer, 256, 3, False)
        layer = AveragePooling2D()(layer)

        feature_vector = Flatten()(layer)

        number_of_ouput_classes = self.number_of_classes
        classification_head = Dense(units=number_of_ouput_classes, kernel_regularizer=l2(self.weight_decay),
                                    activation='softmax', name='output_class')(feature_vector)
        number_of_output_variables = 4  # Four values of the bounding-box: origin-x, origin-y, width and height
        regression_head = Dense(units=number_of_output_variables, kernel_regularizer=l2(self.weight_decay),
                                activation='linear', name='output_bounding_box')(feature_vector)

        model = Model(inputs=[input], outputs=[classification_head, regression_head])
        model.compile(self.get_optimizer(),
                      loss={'output_class': 'categorical_crossentropy', 'output_bounding_box': 'mse'},
                      loss_weights={'output_class': 0.998, 'output_bounding_box': 0.002},
                      metrics=["accuracy"])
        return model

    def add_convolution(self, previous_layer: Layer, filters: int, kernel_size: int):
        layer = Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(self.weight_decay))(
            previous_layer)
        layer = BatchNormalization()(layer)
        layer = Activation('relu')(layer)

        return layer

    def add_res_net_block(self, previous_layer: Layer, filters, kernel_size, shortcut_is_conv) -> Layer:
        layer = Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(self.weight_decay))(
            previous_layer)
        layer = BatchNormalization()(layer)
        layer = Activation('relu')(layer)
        layer = Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(self.weight_decay))(layer)
        layer = BatchNormalization()(layer)

        shortcut = previous_layer
        if shortcut_is_conv:
            shortcut = Convolution2D(filters, kernel_size, padding='same', kernel_regularizer=l2(self.weight_decay))(
                previous_layer)

        merge = add([layer, shortcut])
        layer = Activation('relu')(merge)

        return layer

    def name(self) -> str:
        """ Returns the name of this configuration """
        return "res_net_3_small_with_localization"

    def performs_localization(self) -> bool:
        return True


if __name__ == "__main__":
    configuration = ResNet3SmallWithLocalization("Adadelta", 112, 112, 16, 32)
    classifier = configuration.classifier()
    classifier.summary()
    plot_model(classifier, to_file="res_net_3.png")
    print(configuration.summary())
