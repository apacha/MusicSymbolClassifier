from tensorflow.keras import Input
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer, Activation, BatchNormalization, Convolution2D, Dense, Flatten, MaxPooling2D, AveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import plot_model

from models.TrainingConfiguration import TrainingConfiguration


class Vgg4WithLocalizationConfiguration(TrainingConfiguration):
    """ The winning VGG-Net 4 configuration from Deep Learning course """

    def __init__(self, optimizer, width, height, training_minibatch_size, number_of_classes):
        super().__init__(optimizer=optimizer, data_shape=(height, width, 3),
                         training_minibatch_size=training_minibatch_size, number_of_classes=number_of_classes,
                         number_of_epochs_before_early_stopping=30,
                         number_of_epochs_before_reducing_learning_rate=14)

    def classifier(self) -> Sequential:
        """ Returns the model of this configuration """

        input = Input(shape=self.data_shape)

        layer = self.add_convolution_block_with_batch_normalization(input, 32, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 32, 3)
        layer = MaxPooling2D()(layer)

        layer = self.add_convolution_block_with_batch_normalization(layer, 64, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 64, 3)
        layer = MaxPooling2D()(layer)

        layer = self.add_convolution_block_with_batch_normalization(layer, 128, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 128, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 128, 3)
        layer = MaxPooling2D()(layer)

        layer = self.add_convolution_block_with_batch_normalization(layer, 256, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 256, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 256, 3)
        layer = MaxPooling2D()(layer)

        layer = self.add_convolution_block_with_batch_normalization(layer, 512, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 512, 3)
        layer = self.add_convolution_block_with_batch_normalization(layer, 512, 3)
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
                      metrics=["accuracy"])
        return model

    def add_convolution_block_with_batch_normalization(self, previous_layer: Layer, filters, kernel_size) -> Layer:
        layer = Convolution2D(filters, kernel_size, padding='same',
                              kernel_regularizer=l2(self.weight_decay))(previous_layer)
        layer = BatchNormalization()(layer)
        layer = Activation('relu')(layer)
        return layer

    def name(self) -> str:
        """ Returns the name of this configuration """
        return "vgg4_with_localization"

    def performs_localization(self) -> bool:
        return True


if __name__ == "__main__":
    configuration = Vgg4WithLocalizationConfiguration("Adadelta", 112, 112, 16, 32)
    configuration.classifier().summary()
    plot_model(configuration.classifier(), to_file="vgg4_with_localization.png")
    print(configuration.summary())
