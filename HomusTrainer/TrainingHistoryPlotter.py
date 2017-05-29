import numpy
from keras.callbacks import History
from matplotlib import pyplot


class TrainingHistoryPlotter:
    @staticmethod
    def plot_history(history: History, file_name: str, show_plot: bool = True):
        training_loss = history.history['loss']
        training_accuracy = history.history['acc']
        validation_loss = history.history['val_loss']
        validation_accuracy = history.history['val_acc']

        epoch_list = numpy.add(history.epoch, 1)  # Add 1 so it starts with epoch 1 instead of 0

        fig = pyplot.figure(1)
        # fig.suptitle('TRAINNING vs VALIDATION', fontsize=14, fontweight='bold')

        fig.add_subplot(211)
        pyplot.xlabel("Epoch")
        pyplot.ylabel("Loss")
        pyplot.plot(epoch_list, training_loss, '--', linewidth=2, label='Training loss')
        pyplot.plot(epoch_list, validation_loss, label='Validation loss')
        pyplot.legend(loc='upper right')

        fig.add_subplot(212)
        pyplot.xlabel("Epoch")
        pyplot.ylabel("Accuracy")
        pyplot.plot(epoch_list, training_accuracy, '--', linewidth=2, label='Training accuracy')
        pyplot.plot(epoch_list, validation_accuracy, label='Validation accuracy')
        pyplot.legend(loc='lower right')

        # pyplot.subplots_adjust(wspace=0.1)
        pyplot.tight_layout()
        pyplot.savefig(file_name)

        if show_plot:
            pyplot.show()
