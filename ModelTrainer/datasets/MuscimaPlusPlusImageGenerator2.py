import argparse
import json
import os
from typing import List

from muscima.cropobject import CropObject
from omrdatasettools.image_generators.MuscimaPlusPlusImageGenerator import MuscimaPlusPlusImageGenerator


class MuscimaPlusPlusImageGenerator2(MuscimaPlusPlusImageGenerator):
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
        crop_objects = self.load_crop_objects_from_xml_files(xml_files)
        crop_objects = self.filter_broken_crop_objects(crop_objects)
        crop_objects = self.filter_ignored_crop_objects(crop_objects)

        crop_objects_that_can_be_rendered_directly = self.get_crop_objects_that_can_be_rendered_directly(crop_objects)
        reclassified_crop_objects = self.map_class_names(crop_objects_that_can_be_rendered_directly)
        self.render_masks_of_crop_objects_into_image(reclassified_crop_objects, destination_directory)

        compound_crop_objects = self.process_compound_crop_objects(crop_objects)
        self.render_masks_of_crop_objects_into_image(compound_crop_objects, destination_directory)

    def get_crop_objects_that_can_be_rendered_directly(self, crop_objects: List[CropObject]) -> List[CropObject]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusSymbolClassMapping.json")) as file:
            symbol_class_mapping = json.load(file)
        crop_objects_that_can_be_rendered_directly = [c for c in crop_objects if c.clsname in symbol_class_mapping]
        return crop_objects_that_can_be_rendered_directly

    def filter_broken_crop_objects(self, crop_objects: List[CropObject]):
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusBrokenSymbols.json")) as file:
            broken_crop_objects = json.load(file)
        print("Filtering {0} broken symbols".format(len(broken_crop_objects)))
        crop_objects = [crop_object for crop_object in crop_objects if not crop_object.uid in broken_crop_objects]
        return crop_objects

    def filter_ignored_crop_objects(self, crop_objects: List[CropObject]) -> List[CropObject]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusIgnoredClasses.json")) as file:
            ignored_classes = json.load(file)
        number_of_unfiltered_objects = len(crop_objects)
        crop_objects = [crop_object for crop_object in crop_objects if not crop_object.clsname in ignored_classes]
        number_of_filtered_objects = len(crop_objects)
        print("Filtering {0} symbols from {1} ignored classes".format(
            number_of_unfiltered_objects - number_of_filtered_objects, len(ignored_classes)), flush=True)
        return crop_objects

    def map_class_names(self, crop_objects: List[CropObject]) -> List[CropObject]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusSymbolClassMapping.json")) as file:
            symbol_class_mapping = json.load(file)
        reclassified_crop_objects = crop_objects.copy()
        for crop_object in crop_objects:
            crop_object.clsname = symbol_class_mapping[crop_object.clsname]
        return reclassified_crop_objects

    def process_compound_crop_objects(self, crop_objects: List[CropObject]) -> List[CropObject]:
        print("Processing compound objects ...", flush=True)

        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusClassesThatNeedComposition.json")) as file:
            classes_that_need_composition = json.load(file)

        crop_objects_for_composition = [crop_object for crop_object in crop_objects if
                                        crop_object.clsname in classes_that_need_composition]

        final_crop_objects = []
        quarter_notes = []
        half_notes = []
        eighth_notes = []
        sixteenth_notes = []
        crop_object_dict = {c.uid: c for c in crop_objects}
        for c in crop_objects_for_composition:
            if (c.clsname != 'notehead-full') and (c.clsname != 'notehead-empty'):
                continue

            has_stem = False
            has_beam = False
            has_flag = False
            stem_object = None
            flag_objects = []
            for o in c.outlinks:
                uid_of_outlink = c.dataset + "___" + c.doc + "___" + str(o)
                if not uid_of_outlink in crop_object_dict:
                    continue  # The targeted object has been filtered by broken-list or ignored classes
                outgoing_object = crop_object_dict[uid_of_outlink]
                if outgoing_object.clsname == 'stem':
                    has_stem = True
                    stem_object = outgoing_object
                elif outgoing_object.clsname == 'beam':
                    has_beam = True
                elif outgoing_object.clsname.endswith('flag'):
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
                # We also need to check against quarter-note chords.
                # Stems only have inlinks from noteheads, so checking
                # for multiple inlinks will do the trick.
                if len(stem_object.inlinks) == 1:
                    if c.clsname == 'notehead-full':
                        quarter_notes.append((c, stem_object))
                    else:
                        half_notes.append((c, stem_object))

        for half_note in half_notes:
            note_head, stem = half_note
            note_head.join(stem)
            note_head.clsname = "Half-Note"
            final_crop_objects.append(note_head)

        for quarter_note in quarter_notes:
            note_head, stem = quarter_note
            note_head.join(stem)
            note_head.clsname = "Quarter-Note"
            final_crop_objects.append(note_head)

        for eighth_note in eighth_notes:
            note_head, stem, flags = eighth_note
            note_head.join(stem)
            for flag in flags:
                note_head.join(flag)
            note_head.clsname = "Eighth-Note"
            final_crop_objects.append(note_head)

        for sixteenth_note in sixteenth_notes:
            note_head, stem, flags = sixteenth_note
            note_head.join(stem)
            for flag in flags:
                note_head.join(flag)
            note_head.clsname = "Sixteenth-Note"
            final_crop_objects.append(note_head)

        return final_crop_objects


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
