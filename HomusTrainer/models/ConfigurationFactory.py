from models import TrainingConfiguration
from models.SimpleConfiguration import SimpleConfiguration
from models.Vgg4Configuration import Vgg4Configuration
from models.Vgg4WithLocalization import Vgg4WithLocalizationConfiguration
from models.VggConfiguration import VggConfiguration


class ConfigurationFactory:
    @staticmethod
    def get_configuration_by_name(name: str = "simple",
                                  optimizer="Adadelta",
                                  width=128,
                                  height=224,
                                  training_minibatch_size=64) -> TrainingConfiguration:
        configurations = []
        configurations.append(SimpleConfiguration())
        configurations.append(VggConfiguration(optimizer, width, height, training_minibatch_size))
        configurations.append(Vgg4Configuration(optimizer, width, height, training_minibatch_size))
        configurations.append(Vgg4WithLocalizationConfiguration(optimizer, width, height, training_minibatch_size))

        for i in range(len(configurations)):
            if configurations[i].name() == name:
                return configurations[i]

        raise Exception("No configuration found by name {0}".format(name))
