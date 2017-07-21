from models import TrainingConfiguration
from models.ResNet2Configuration import ResNet2Configuration
from models.ResNet1Configuration import ResNet1Configuration
from models.ResNet3Configuration import ResNet3Configuration
from models.ResNet3SmallConfiguration import ResNet3SmallConfiguration
from models.ResNet4Configuration import ResNet4Configuration
from models.ResNet5Configuration import ResNet5Configuration
from models.ResNet5SmallConfiguration import ResNet5SmallConfiguration
from models.SimpleConfiguration import SimpleConfiguration
from models.Vgg4Configuration import Vgg4Configuration
from models.Vgg4WithLocalization import Vgg4WithLocalizationConfiguration
from models.VggConfiguration import VggConfiguration


class ConfigurationFactory:
    @staticmethod
    def get_configuration_by_name(name: str,
                                  optimizer: str,
                                  width: int,
                                  height: int,
                                  training_minibatch_size: int,
                                  number_of_classes: int) -> TrainingConfiguration:
        configurations = []
        configurations.append(SimpleConfiguration(optimizer, width, height, training_minibatch_size,number_of_classes))
        configurations.append(VggConfiguration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(Vgg4Configuration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet1Configuration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet2Configuration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet3Configuration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet3SmallConfiguration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet4Configuration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet5Configuration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(ResNet5SmallConfiguration(optimizer, width, height, training_minibatch_size, number_of_classes))
        configurations.append(Vgg4WithLocalizationConfiguration(optimizer, width, height, training_minibatch_size, number_of_classes))

        for i in range(len(configurations)):
            if configurations[i].name() == name:
                return configurations[i]

        raise Exception("No configuration found by name {0}".format(name))
