import numpy
from tensorflow.keras.callbacks import History
from matplotlib import pyplot


class TrainingHistoryPlotter:
    @staticmethod
    def plot_history(history: History, file_name: str, show_plot: bool = False):
        epoch_list = numpy.add(history.epoch, 1)  # Add 1 so it starts with epoch 1 instead of 0

        fig = pyplot.figure(1)
        # fig.suptitle('TRAINNING vs VALIDATION', fontsize=14, fontweight='bold')

        # Regular plot for classification only
        if "val_accuracy" in history.history:
            TrainingHistoryPlotter.add_subplot(epoch_list, fig, history, 211, "Loss", "loss", "Training loss",
                                               "val_loss",
                                               "Validation loss", "upper right")
            TrainingHistoryPlotter.add_subplot(epoch_list, fig, history, 212, "Accuracy", "accuracy", "Training accuracy",
                                               "val_accuracy",
                                               "Validation accuracy", "lower right")
        else:
            TrainingHistoryPlotter.add_subplot(epoch_list, fig, history, 221, "Classification Loss",
                                               "output_class_loss",
                                               "Training loss", "val_output_class_loss",
                                               "Validation loss", "upper right")
            TrainingHistoryPlotter.add_subplot(epoch_list, fig, history, 222, "Classification Accuracy",
                                               "output_class_acc", "Training accuracy", "val_output_class_acc",
                                               "Validation accuracy", "lower right")
            TrainingHistoryPlotter.add_subplot(epoch_list, fig, history, 223, "Bounding-Box Loss",
                                               "output_bounding_box_loss", "Training loss",
                                               "val_output_bounding_box_loss", "Validation loss", "upper right")
            TrainingHistoryPlotter.add_subplot(epoch_list, fig, history, 224, "Bounding-Box Accuracy",
                                               "output_bounding_box_acc", "Training accuracy",
                                               "val_output_bounding_box_acc", "Validation accuracy", "lower right")

        # pyplot.subplots_adjust(wspace=0.1)
        pyplot.tight_layout()
        pyplot.savefig(file_name)

        if show_plot:
            pyplot.show()

    @staticmethod
    def add_subplot(epoch_list, fig, history, subplot_region, y_axis_label,
                    history_parameter1, parameter1_label,
                    history_parameter2, parameter2_label, legend_position):
        fig.add_subplot(subplot_region)
        pyplot.xlabel("Epoch")
        pyplot.ylabel(y_axis_label)
        pyplot.plot(epoch_list, history.history[history_parameter1], '--', linewidth=2, label=parameter1_label)
        pyplot.plot(epoch_list, history.history[history_parameter2], label=parameter2_label)
        pyplot.legend(loc=legend_position)
