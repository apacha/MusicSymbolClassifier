import argparse
import json
import os
from glob import glob
from typing import List

import sys

from PIL import Image
from muscima.io import parse_cropobject_list
from tqdm import tqdm

from datasets.ExportPath import ExportPath
from muscima.cropobject import CropObject


class MuscimaPlusPlusImageGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))

    def extract_all_symbols_as_they_are(self, raw_data_directory: str, destination_directory: str):
        """
        Extracts all symbols from the raw XML documents and generates individual symbols from the masks

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        """
        print("Extracting Symbols from Muscima++ Dataset...")

        xml_files = self.__load_all_xml_files(raw_data_directory)
        crop_objects = self.__load_crop_objects_from_xml_files(xml_files)
        self.__render_masks_of_crop_objects_into_image(crop_objects, destination_directory)

    def extract_symbols_for_training(self, raw_data_directory: str, destination_directory: str):
        """
        Extracts all symbols from the raw XML documents and generates individual symbols from the masks.
        This method filters broken symbols, performs a re-classification and joins individual
        symbols into larger symbols for meeting the required classes of the other datasets.

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        """
        print("Extracting Symbols from Muscima++ Dataset...")

        xml_files = self.__load_all_xml_files(raw_data_directory)
        crop_objects = self.__load_crop_objects_from_xml_files(xml_files)
        crop_objects = self.__filter_broken_crop_objects(crop_objects)
        crop_objects = self.__filter_ignored_crop_objects(crop_objects)

        crop_objects_that_can_be_rendered_directly = self.__get_crop_objects_that_can_be_rendered_directly(crop_objects)
        reclassified_crop_objects = self.__map_class_names(crop_objects_that_can_be_rendered_directly)
        self.__render_masks_of_crop_objects_into_image(reclassified_crop_objects, destination_directory)

        compound_crop_objects = self.__process_compound_crop_objects(crop_objects)
        self.__render_masks_of_crop_objects_into_image(compound_crop_objects, destination_directory)

    def __get_crop_objects_that_can_be_rendered_directly(self, crop_objects: List[CropObject]) -> List[CropObject]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusSymbolClassMapping.json")) as file:
            symbol_class_mapping = json.load(file)
        crop_objects_that_can_be_rendered_directly = [c for c in crop_objects if c.clsname in symbol_class_mapping]
        return crop_objects_that_can_be_rendered_directly

    def __load_all_xml_files(self, raw_data_directory: str) -> List[str]:
        raw_data_directory = os.path.join(raw_data_directory, "v0.9", "data", "cropobjects")
        xml_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.xml'))]
        return xml_files

    def __load_crop_objects_from_xml_files(self, xml_files: List[str]) -> List[CropObject]:
        crop_objects = []
        for xml_file in tqdm(xml_files, desc="Loading crop-objects from xml-files", smoothing=0.1, mininterval=0.25):
            crop_objects.extend(self.__get_crop_objects_from_xml_file(xml_file))

        for crop_object in crop_objects:
            # Some classes have special characters in their class name that we have to remove
            crop_object.clsname = crop_object.clsname.replace('"', '').replace('/', '').replace('.', '')

        print("Loaded {0} crop-objects".format(len(crop_objects)))
        return crop_objects

    def __get_crop_objects_from_xml_file(self, xml_file: str) -> List[CropObject]:
        # e.g., xml_file = 'data/muscima_pp/v0.9/data/cropobjects/CVC-MUSCIMA_W-01_N-10_D-ideal.xml'
        crop_objects = parse_cropobject_list(xml_file)
        return crop_objects

    def __filter_broken_crop_objects(self, crop_objects: List[CropObject]):
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusBrokenSymbols.json")) as file:
            broken_crop_objects = json.load(file)
        print("Filtering {0} broken symbols".format(len(broken_crop_objects)))
        crop_objects = [crop_object for crop_object in crop_objects if not crop_object.uid in broken_crop_objects]
        return crop_objects

    def __filter_ignored_crop_objects(self, crop_objects: List[CropObject]) -> List[CropObject]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusIgnoredClasses.json")) as file:
            ignored_classes = json.load(file)
        number_of_unfiltered_objects = len(crop_objects)
        crop_objects = [crop_object for crop_object in crop_objects if not crop_object.clsname in ignored_classes]
        number_of_filtered_objects = len(crop_objects)
        print("Filtering {0} symbols from {1} ignored classes".format(
            number_of_unfiltered_objects - number_of_filtered_objects, len(ignored_classes)))
        return crop_objects

    def __map_class_names(self, crop_objects: List[CropObject]) -> List[CropObject]:
        with open(os.path.join(self.path_of_this_file, "MuscimaPlusPlusSymbolClassMapping.json")) as file:
            symbol_class_mapping = json.load(file)
        reclassified_crop_objects = crop_objects.copy()
        for crop_object in crop_objects:
            crop_object.clsname = symbol_class_mapping[crop_object.clsname]
        return reclassified_crop_objects

    def __process_compound_crop_objects(self, crop_objects: List[CropObject]) -> List[CropObject]:
        print("Processing compound objects ...")

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

    def __render_masks_of_crop_objects_into_image(self, crop_objects: List[CropObject], destination_directory: str):
        for crop_object in tqdm(crop_objects, desc="Generating images from crop-object masks", smoothing=0.1,
                                mininterval=0.25):
            symbol_class = crop_object.clsname
            # Make a copy of the mask to not temper with the original data
            mask = crop_object.mask.copy()
            # We want to draw black symbols on white canvas. The mask encodes foreground pixels
            # that we are interested in with a 1 and background pixels with a 0 and stores those values in
            # an uint8 numpy array. To use Image.fromarray, we have to generate a greyscale mask, where
            # white pixels have the value 255 and black pixels have the value 0. To achieve this, we simply
            # subtract one from each uint, and by exploiting the underflow of the uint we get the following mapping:
            # 0 (background) => 255 (white) and 1 (foreground) => 0 (black) which is exactly what we wanted.
            mask -= 1
            image = Image.fromarray(mask, mode="L")

            target_directory = os.path.join(destination_directory, symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            export_path = ExportPath(destination_directory, symbol_class, crop_object.uid)
            image.save(export_path.get_full_path())


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

    muscima_pp_image_generator = MuscimaPlusPlusImageGenerator()
    muscima_pp_image_generator.extract_symbols_for_training(flags.raw_dataset_directory, flags.image_dataset_directory)
    # muscima_pp_image_generator.extract_all_symbols_as_they_are(flags.raw_dataset_directory,
    #                                                            flags.image_dataset_directory)
