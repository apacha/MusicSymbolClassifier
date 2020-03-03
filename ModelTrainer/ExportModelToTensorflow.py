import argparse
import os
import shutil

import tensorflow.keras
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.core.protobuf import saver_pb2
from tensorflow.python.framework import graph_io
from tensorflow.python.tools import freeze_graph

tensorflow.keras.backend.set_learning_phase(0)  # all new operations will be in test mode from now on


def export_model_to_tensorflow(path_to_trained_keras_model: str):
    print("Loading model for exporting to Protocol Buffer format...")
    model = tensorflow.keras.models.load_model(path_to_trained_keras_model)

    sess = tensorflow.keras.backend.get_session()

    # serialize the model and get its weights, for quick re-building
    config = model.get_config()
    weights = model.get_weights()

    # re-build a model where the learning phase is now hard-coded to 0
    new_model = Sequential.from_config(config)
    new_model.set_weights(weights)

    export_path = os.path.abspath(os.path.join("export", "simple"))  # where to save the exported graph
    os.makedirs(export_path)
    checkpoint_state_name = "checkpoint_state"
    export_version = 1  # version number (integer)
    saver = tensorflow.train.Saver(sharded=True, name=checkpoint_state_name)
    model_exporter = exporter.Exporter(saver)
    signature = exporter.classification_signature(input_tensor=model.input, scores_tensor=model.output)

    # # Version 1 of exporter
    # model_exporter.init(sess.graph.as_graph_def(), default_graph_signature=signature)
    # model_exporter.export(export_path, tensorflow.constant(export_version), sess)
    #
    # # Version 2 of exporter
    # tensorflow.train.write_graph(sess.graph.as_graph_def(), logdir=".", name="simple.pbtxt", as_text=True)

    # Version 3 with Freezer from https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/tools/freeze_graph_test.py
    input_graph_name = "input_graph.pb"
    output_graph_name = "output_graph.pb"
    saver_write_version = saver_pb2.SaverDef.V2

    # We'll create an input graph that has a single variable containing 1.0,
    # and that then multiplies it by 2.
    saver = tensorflow.train.Saver(write_version=saver_write_version)
    checkpoint_path = saver.save(sess, export_path, global_step=0, latest_filename=checkpoint_state_name)
    graph_io.write_graph(sess.graph, export_path, input_graph_name)

    # We save out the graph to disk, and then call the const conversion
    # routine.
    input_graph_path = os.path.join(export_path, input_graph_name)
    input_saver_def_path = ""
    input_binary = False
    output_node_names = "output_node/Softmax"
    restore_op_name = "save/restore_all"
    filename_tensor_name = "save/Const:0"
    output_graph_path = os.path.join(export_path, output_graph_name)
    clear_devices = False
    freeze_graph.freeze_graph(input_graph_path, input_saver_def_path,
                              input_binary, checkpoint_path, output_node_names,
                              restore_op_name, filename_tensor_name,
                              output_graph_path, clear_devices, "")

    shutil.copy(os.path.join("export", "simple", "output_graph.pb"), output_graph_name)
    shutil.rmtree("export")
    print("Exported model: {0}".format(os.path.abspath(output_graph_name)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_to_trained_keras_model",
        type=str,
        default="vgg.h5",
        help="The path to the file that containes the trained keras model that should be converted to a Protobuf file")

    flags, unparsed = parser.parse_known_args()

    export_model_to_tensorflow(flags.path_to_trained_keras_model)
