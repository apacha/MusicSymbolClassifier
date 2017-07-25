import argparse
import os
from glob import glob
from xml.etree import ElementTree

from PIL import Image
from sympy import Point2D

from datasets.ExportPath import ExportPath
from datasets.Rectangle import Rectangle


class AudiverisOmrImageGenerator:
    def extract_symbols(self, raw_data_directory: str, destination_directory: str):
        """
        Extracts the symbols from the raw XML documents and matching images of the Audiveris OMR dataset into
        individual symbols

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        """
        print("Extracting Symbols from Audiveris OMR Dataset...")

        all_xml_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.xml'))]
        all_image_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.png'))]

        data_pairs = []
        for i in range(len(all_xml_files)):
            data_pairs.append((all_xml_files[i], all_image_files[i]))

        for data_pair in data_pairs:
            self.__extract_symbols(data_pair[0], data_pair[1], destination_directory)

    def __extract_symbols(self, xml_file: str, image_file: str, destination_directory: str):
        class_substitution_map = {"accidentalFlat": "Flat",
                                  "accidentalNatural": "Natural",
                                  "accidentalSharp": "Sharp",
                                  "articStaccatissimoAbove": "Staccatissimo",
                                  "articStaccatoAbove": "Dot",
                                  "articTenutoBelow": "Tenuto",
                                  "augmentationDot": "Dot",
                                  "barlineDouble": "Barline",
                                  "barlineSingle": "Barline",
                                  "brace": "Brace",
                                  "coda": "Coda",
                                  "codaSquare": "Coda-Square",
                                  "dynamicMP": "Other",
                                  "dynamicPiano": "Other",
                                  "fClef": "F-Clef",
                                  "fClefChange": "F-Clef",
                                  "flag8thDown": "Eighth-Flag",
                                  "flag8thUp": "Eighth-Flag",
                                  "flag16thUp": "Sixteenth-Flag",
                                  "flag32ndUp": "Thirty-Two-Flag",
                                  "flag128thDown": "Onehundred-Twenty-Eight-Flag",
                                  "gClef": "G-Clef",
                                  "gClefChange": "G-Clef",
                                  "graceNoteAcciaccaturaStemUp": "Eighth-Grace-Note",
                                  "graceNoteApporggiaturaStempUp": "Eighth-Note",
                                  "keyFlat": "Flat",
                                  "keySharp": "Sharp",
                                  "noteheadBlack": "Full-Note-Head",
                                  "noteheadBlackSmall": "Full-Note-Head",
                                  "noteheadHalf": "Half-Note-Head",
                                  "noteheadWhole": "Whole-Note",
                                  "rest8th": "Eighth-Rest",
                                  "rest16th": "Sixteenth-Rest",
                                  "rest32th": "Thirty-Two-Rest",
                                  "rest64th": "Sixty-Four-Rest",
                                  "rest128th": "Onehundred-Twenty-Eight-Rest",
                                  "restHalf": "Whole-Half-Rest",
                                  "restQuarter": "Quarter-Rest",
                                  "restWhole": "Whole-Half-Rest",
                                  "segno": "Segno",
                                  "stem": "Stem",
                                  "timeSig4over4": "4-4-Time",
                                  "timeSigCommon": "Common-Time",
                                  "timeSigCutCommon": "Cut-Time",
                                  "tuplet3": "Other"}
        note_head_classes_for_refinement = ["Full-Note-Head", "Half-Note-Head"]
        stem_class_for_refinement = "Stem"
        flag_classes_for_refinement = ["Eight-Flag", "Sixteenth-Flag", "Thirdy-Two-Flag",
                                       "Onehundred-Twenty-Eight-Flag"]

        ignored_classes = ["ledger"]

        # Everything about should be moved somewhere else

        # xml_file, image_file = 'data/audiveris_omr_raw\\IMSLP06053p1.xml', 'data/audiveris_omr_raw\\IMSLP06053p1.png'
        # xml_file, image_file = 'data/audiveris_omr_raw\\mops-1.xml', 'data/audiveris_omr_raw\\mops-1.png'
        # xml_file, image_file = 'data/audiveris_omr_raw\\mtest1-1.xml', 'data/audiveris_omr_raw\\mtest1-1.png'
        # xml_file, image_file = 'data/audiveris_omr_raw\\mtest2-1.xml', 'data/audiveris_omr_raw\\mtest2-1.png'
        image = Image.open(image_file)
        annotations = ElementTree.parse(xml_file).getroot()
        xml_symbols = annotations.findall("Symbol")

        file_name_without_extension = os.path.splitext(os.path.basename(xml_file))[0]
        symbols = []
        stems = []
        note_heads = []
        note_head_flags = []

        for xml_symbol in xml_symbols:
            symbol_class = xml_symbol.get("shape")

            if symbol_class in ignored_classes:
                continue  # Ignored classes will be skipped

            mapped_symbol_class = class_substitution_map[symbol_class]

            bounds = xml_symbol.find("Bounds")
            x, y, width, height = bounds.get("x"), bounds.get("y"), bounds.get("w"), bounds.get("h")
            x, y, width, height = int(float(x)), int(float(y)), int(float(width)), int(float(height))

            symbol = AudiverisOmrSymbol(mapped_symbol_class, x, y, width, height)

            if mapped_symbol_class in note_head_classes_for_refinement:
                note_heads.append(symbol)
            elif mapped_symbol_class in flag_classes_for_refinement:
                note_head_flags.append(symbol)
            elif mapped_symbol_class == stem_class_for_refinement:
                stems.append(symbol)
            else:
                symbols.append(symbol)

        pairs = []

        for half_note_head in [s for s in note_heads if s.symbol_class == "Half-Note-Head"]:
            for stem in stems:
                if Rectangle.overlap(half_note_head, stem):
                    pairs.append((half_note_head, stem))

        i = 0
        for pair in pairs:
            symbol_class = pair[0].symbol_class
            merge = Rectangle.merge(pair[0], pair[1])
            bounding_box_with_one_pixel_margin = merge.as_bounding_box_with_margin(1)
            symbol_image = image.crop(bounding_box_with_one_pixel_margin)

            target_directory = os.path.join(destination_directory, symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            export_path = ExportPath(destination_directory, symbol_class, file_name_without_extension + str(i))
            symbol_image.save(export_path.get_full_path())
            i += 1


class AudiverisOmrSymbol(Rectangle):
    def __init__(self, symbol_class: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__(Point2D(x, y), width, height)
        self.symbol_class = symbol_class


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--raw_dataset_directory",
            type=str,
            default="../data/audiveris_omr_raw",
            help="The directory, where the raw Audiveris OMR dataset can be found")
    parser.add_argument(
            "--image_dataset_directory",
            type=str,
            default="../data/images",
            help="The directory, where the generated bitmaps will be created")

    flags, unparsed = parser.parse_known_args()

    audiveris_omr_image_generator = AudiverisOmrImageGenerator()
    audiveris_omr_image_generator.extract_symbols(flags.raw_dataset_directory, flags.image_dataset_directory)
