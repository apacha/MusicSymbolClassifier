import argparse
import json
import os
from typing import List, Dict

from mung.node import Node
from omrdatasettools.MuscimaPlusPlusSymbolImageGenerator import MuscimaPlusPlusSymbolImageGenerator


class MuscimaPlusPlusImageGenerator2(MuscimaPlusPlusSymbolImageGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))

    def extract_symbols_for_training(self, raw_data_directory: str, destination_directory: str):
        """
        Extracts all symbols from the raw XML documents and generates individual symbols from the masks.
        This method filters broken symbols, performs a re-classification and joins individual
        symbols into larger symbols for meeting the required classes of the other datasets.

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        """
        print("Extracting Symbols from Muscima++ Dataset...", flush=True)

        xml_files = self.get_all_xml_file_paths(raw_data_directory)
        nodes = self.load_nodes_from_xml_files(xml_files)
        nodes = self.filter_broken_nodes(nodes)
        nodes = self.filter_ignored_nodes(nodes)

        nodes_that_can_be_rendered_directly = self.get_nodes_that_can_be_rendered_directly(nodes)
        reclassified_nodes = self.map_class_names(nodes_that_can_be_rendered_directly)
        self.render_masks_of_nodes_into_image(reclassified_nodes, destination_directory)

        compound_nodes = self.process_compound_nodes(nodes)
        self.render_masks_of_nodes_into_image(compound_nodes, destination_directory)

    def get_nodes_that_can_be_rendered_directly(self, nodes: List[Node]) -> List[Node]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusSymbolClassMapping.json")) as file:
            symbol_class_mapping = json.load(file)
        nodes_that_can_be_rendered_directly = [c for c in nodes if c.class_name in symbol_class_mapping]
        return nodes_that_can_be_rendered_directly

    def filter_broken_nodes(self, nodes: List[Node]):
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusBrokenSymbols.json")) as file:
            broken_nodes = json.load(file)
        print("Filtering {0} broken symbols".format(len(broken_nodes)))
        nodes = [node for node in nodes if not node.unique_id in broken_nodes]
        return nodes

    def filter_ignored_nodes(self, nodes: List[Node]) -> List[Node]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusIgnoredClasses.json")) as file:
            ignored_classes = json.load(file)
        number_of_unfiltered_objects = len(nodes)
        nodes = [node for node in nodes if node.class_name not in ignored_classes]
        number_of_filtered_objects = len(nodes)
        print("Filtering {0} symbols from {1} ignored classes".format(
            number_of_unfiltered_objects - number_of_filtered_objects, len(ignored_classes)), flush=True)
        return nodes

    def map_class_names(self, nodes: List[Node]) -> List[Node]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusSymbolClassMapping.json")) as file:
            symbol_class_mapping = json.load(file)
        reclassified_nodes = []
        for node in nodes:
            reclassified_nodes.append(
                Node(node.id, symbol_class_mapping[node.class_name], node.top, node.left, node.width, node.height,
                     node.outlinks, node.inlinks, node.mask, node.dataset, node.document, node.data))
        return reclassified_nodes

    def process_compound_nodes(self, nodes: List[Node]) -> List[Node]:
        print("Processing compound objects ...", flush=True)

        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusClassesThatNeedComposition.json")) as file:
            classes_that_need_composition = json.load(file)

        nodes_for_composition = [node for node in nodes if
                                 node.class_name in classes_that_need_composition]

        final_nodes = []
        quarter_notes = []
        half_notes = []
        eighth_notes = []
        sixteenth_notes = []
        node_dict = {c.unique_id: c for c in nodes}  # type: Dict[str, Node]
        for c in nodes_for_composition:
            if c.class_name not in ['noteheadFull', 'noteheadHalf']:
                continue

            has_stem = False
            has_beam = False
            has_flag = False
            stem_object = None
            flag_objects = []
            for o in c.outlinks:
                uid_of_outlink = Node.UID_DELIMITER.join([c.dataset, c.document, str(o)])
                if uid_of_outlink not in node_dict:
                    continue  # The targeted object has been filtered by broken-list or ignored classes
                outgoing_object = node_dict[uid_of_outlink]
                if outgoing_object.class_name == 'stem':
                    has_stem = True
                    stem_object = outgoing_object
                elif outgoing_object.class_name == 'beam':
                    has_beam = True
                elif outgoing_object.class_name.startswith('flag'):
                    has_flag = True
                    flag_objects.append(outgoing_object)

            if not has_stem:
                continue

            if has_beam:
                pass
            elif has_flag:
                if len(flag_objects) == 1:
                    eighth_notes.append((c, stem_object, flag_objects))
                elif len(flag_objects) == 2:
                    sixteenth_notes.append((c, stem_object, flag_objects))
            else:
                if c.class_name == 'noteheadFull':
                    quarter_notes.append((c, stem_object))
                else:
                    half_notes.append((c, stem_object))

        for half_note in half_notes:
            note_head, stem = half_note
            note_head.join(stem)
            final_nodes.append(
                Node(note_head.id, "Half-Note", note_head.top, note_head.left, note_head.width, note_head.height,
                     note_head.outlinks, note_head.inlinks, note_head.mask, note_head.dataset, note_head.document,
                     note_head.data))

        for quarter_note in quarter_notes:
            note_head, stem = quarter_note
            note_head.join(stem)
            final_nodes.append(
                Node(note_head.id, "Quarter-Note", note_head.top, note_head.left, note_head.width, note_head.height,
                     note_head.outlinks, note_head.inlinks, note_head.mask, note_head.dataset, note_head.document,
                     note_head.data))

        for eighth_note in eighth_notes:
            note_head, stem, flags = eighth_note
            note_head.join(stem)
            for flag in flags:
                note_head.join(flag)
            final_nodes.append(
                Node(note_head.id, "Eighth-Note", note_head.top, note_head.left, note_head.width, note_head.height,
                     note_head.outlinks, note_head.inlinks, note_head.mask, note_head.dataset, note_head.document,
                     note_head.data))

        for sixteenth_note in sixteenth_notes:
            note_head, stem, flags = sixteenth_note
            note_head.join(stem)
            for flag in flags:
                note_head.join(flag)
            final_nodes.append(
                Node(note_head.id, "Sixteenth-Note", note_head.top, note_head.left, note_head.width, note_head.height,
                     note_head.outlinks, note_head.inlinks, note_head.mask, note_head.dataset, note_head.document,
                     note_head.data))

        return final_nodes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/muscima_pp_raw",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the generated bitmaps will be created")

    flags, unparsed = parser.parse_known_args()

    muscima_pp_image_generator = MuscimaPlusPlusImageGenerator2()
    muscima_pp_image_generator.extract_symbols_for_training(flags.raw_dataset_directory, flags.image_dataset_directory)
