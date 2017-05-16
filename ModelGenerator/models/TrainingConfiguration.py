from abc import ABC, abstractmethod

from keras.engine import Model


class TrainingConfiguration(ABC):
    def __init__(self,
                 data_shape: tuple = (256, 256, 3),
                 number_of_epochs: int = 200,
                 number_of_epochs_before_early_stopping: int = 10,
                 number_of_epochs_before_reducing_learning_rate: int = 5,
                 training_minibatch_size: int = 16,
                 initialization: str = "he_normal",
                 learning_rate: float = 0.001,
                 learning_rate_reduction_factor: float = 0.5,
                 minimum_learning_rate: float = 0.0001,
                 weight_decay: float = 0.0001,
                 nesterov_momentum: float = 0.9,
                 number_of_pixel_shift=24.0
                 ):
        self.data_shape = data_shape
        self.number_of_epochs = number_of_epochs
        self.number_of_epochs_before_early_stopping = number_of_epochs_before_early_stopping
        self.number_of_epochs_before_reducing_learning_rate = number_of_epochs_before_reducing_learning_rate
        self.training_minibatch_size = training_minibatch_size
        self.initialization = initialization
        self.learning_rate = learning_rate
        self.learning_rate_reduction_factor = learning_rate_reduction_factor
        self.minimum_learning_rate = minimum_learning_rate
        self.weight_decay = weight_decay
        self.nesterov_momentum = nesterov_momentum
        self.number_of_pixel_shift = number_of_pixel_shift

    @abstractmethod
    def classifier(self) -> Model:
        """ Returns the classifier of this configuration """
        pass

    @abstractmethod
    def name(self) -> str:
        """ Returns the name of this configuration """
        pass

    def summary(self) -> str:
        """ Returns the string that summarizes this configuration """
        summary = "Training for {0:d} epochs with initial learning rate of {1}, weight-decay of {2} and Nesterov Momentum of {3} ...\n" \
            .format(self.number_of_epochs, self.learning_rate, self.weight_decay, self.nesterov_momentum)
        summary += "Additional parameters: Initialization: {0}, Minibatch-size: {1}, Early stopping after {2} epochs without improvement\n" \
            .format(self.initialization, self.training_minibatch_size, self.number_of_epochs_before_early_stopping)
        summary += "Data-Shape: {0}, Reducing learning rate by factor to {1} respectively if not improved validation accuracy after {2} epochs" \
            .format(self.data_shape, self.learning_rate_reduction_factor,
                    self.number_of_epochs_before_reducing_learning_rate)
        return summary
