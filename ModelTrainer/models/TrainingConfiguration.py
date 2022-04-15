from abc import ABC, abstractmethod

from tensorflow.keras import Model
from tensorflow.keras.optimizers import Optimizer, SGD, Adam, Adadelta


class TrainingConfiguration(ABC):
    """ The base class for a configuration that specifies the hyperparameters of a training """

    def __init__(self,
                 data_shape: tuple = (224, 128, 3),  # Rows = Height, columns = Width, channels = typically 3 (RGB)
                 number_of_classes: int = 32,
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
                 optimizer: str = "SGD",
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
        self.number_of_classes = number_of_classes
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

    @abstractmethod
    def performs_localization(self) -> bool:
        """ Returns wether this configuration has a regression head that performs object localization or not """
        pass

    def get_optimizer(self) -> Optimizer:
        """
        Returns the configured optimizer for this configuration
        :return:
        """
        if self.optimizer == "SGD":
            return SGD(lr=self.learning_rate, momentum=self.nesterov_momentum, nesterov=True)
        if self.optimizer == "Adam":
            return Adam()
        if self.optimizer == "Adadelta":
            return Adadelta()

        raise Exception("Invalid optimizer {0} requested".format(self.optimizer))

    def get_initial_learning_rate(self) -> float:
        cfg = self.get_optimizer().get_config()
        if "lr" in cfg:
            return cfg["lr"]
        else:
            return cfg["learning_rate"]

    def summary(self) -> str:
        """ Returns the string that summarizes this configuration """

        optimizer = self.get_optimizer()

        summary = "Training for {0:d} epochs ...\n".format(self.number_of_epochs)
        summary += "Additional parameters: Initialization: {0}, Weight-decay of {1}, Minibatch-size: {2}, " \
                   "Early stopping after {3} epochs without improvement\n" \
            .format(self.initialization, self.weight_decay, self.training_minibatch_size,
                    self.number_of_epochs_before_early_stopping)
        summary += "Data-Shape: {0}, Reducing learning rate by factor to {1} respectively if not improved validation " \
                   "accuracy after {2} epochs\n" \
            .format(self.data_shape, self.learning_rate_reduction_factor,
                    self.number_of_epochs_before_reducing_learning_rate)
        summary += "Data-augmentation: Zooming {0}% randomly, rotating {1}° randomly\n" \
            .format(self.zoom_range * 100, self.rotation_range)
        summary += "Optimizer: {0}, with parameters {1}\n".format(self.optimizer, optimizer.get_config())
        summary += "Performing object localization: {0}".format(self.performs_localization())

        return summary
