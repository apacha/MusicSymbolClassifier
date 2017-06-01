from abc import ABC, abstractmethod

from keras.engine import Model
from keras.optimizers import Optimizer, SGD, Adam, Adadelta


class TrainingConfiguration(ABC):
    def __init__(self,
                 data_shape: tuple = (224, 128, 3),  # Rows, columns, channels
                 number_of_epochs: int = 200,
                 number_of_epochs_before_early_stopping: int = 20,
                 number_of_epochs_before_reducing_learning_rate: int = 8,
                 training_minibatch_size: int = 64,
                 initialization: str = "glorot_uniform",
                 learning_rate: float = 0.01,
                 learning_rate_reduction_factor: float = 0.5,
                 minimum_learning_rate: float = 0.00001,
                 weight_decay: float = 0.0001,
                 nesterov_momentum: float = 0.9,
                 zoom_range=0.2,
                 rotation_range=10,
                 optimizer: str = "SGD"
                 ):
        """
        :param data_shape: Tuple with order (rows, columns, channels)
        :param zoom_range: Percentage that the input will dynamically be zoomed turing training (0-1)
        :param rotation_range: Random rotation of the input image during training in degree
        :param optimizer: The used optimizer for the training, currently supported are either 'SGD', 'Adam' or 'Adadelta'.
        """
        self.optimizer = optimizer
        self.rotation_range = rotation_range
        self.data_shape = data_shape
        self.input_image_rows, self.input_image_columns, self.input_image_channels = data_shape
        self.number_of_epochs = number_of_epochs
        self.zoom_range = zoom_range
        self.number_of_epochs_before_early_stopping = number_of_epochs_before_early_stopping
        self.number_of_epochs_before_reducing_learning_rate = number_of_epochs_before_reducing_learning_rate
        self.training_minibatch_size = training_minibatch_size
        self.initialization = initialization
        self.learning_rate = learning_rate
        self.learning_rate_reduction_factor = learning_rate_reduction_factor
        self.minimum_learning_rate = minimum_learning_rate
        self.weight_decay = weight_decay
        self.nesterov_momentum = nesterov_momentum

    @abstractmethod
    def classifier(self) -> Model:
        """ Returns the classifier of this configuration """
        pass

    @abstractmethod
    def name(self) -> str:
        """ Returns the name of this configuration """
        pass

    def get_optimizer(self) -> Optimizer:
        """
        Returns the configured optimizer for this configuration
        :return:
        """
        if self.optimizer == "SGD":
            return SGD(lr=self.learning_rate, momentum=self.nesterov_momentum, nesterov=True)
        if self.optimizer == "Adam":
            return Adam(lr=self.learning_rate)
        if self.optimizer == "Adadelta":
            return Adadelta()

        raise Exception("Invalid optimizer {0} requested".format(self.optimizer))

    def summary(self) -> str:
        """ Returns the string that summarizes this configuration """

        optimizer = self.get_optimizer()

        summary = "Training for {0:d} epochs with initial learning rate of {1}, weight-decay of {2} and Nesterov Momentum of {3} ...\n" \
            .format(self.number_of_epochs, self.learning_rate, self.weight_decay, self.nesterov_momentum)
        summary += "Additional parameters: Initialization: {0}, Minibatch-size: {1}, Early stopping after {2} epochs without improvement\n" \
            .format(self.initialization, self.training_minibatch_size, self.number_of_epochs_before_early_stopping)
        summary += "Data-Shape: {0}, Reducing learning rate by factor to {1} respectively if not improved validation accuracy after {2} epochs\n" \
            .format(self.data_shape, self.learning_rate_reduction_factor,
                    self.number_of_epochs_before_reducing_learning_rate)
        summary += "Data-augmentation: Zooming {0}% randomly, rotating {1}° randomly\n" \
            .format(self.zoom_range * 100, self.rotation_range)
        summary += "Optimizer: {0}, with parameters {1}".format(self.optimizer, optimizer.get_config())
        return summary
