import os


class ExportPath:
    def __init__(self, destination_directory: str, symbol_class: str, raw_file_name_without_extension: str,
                 stroke_thickness: int, extension: str = "png") -> None:
        super().__init__()
        self.stroke_thickness = stroke_thickness
        self.extension = extension
        self.raw_file_name_without_extension = raw_file_name_without_extension
        self.symbol_class = symbol_class
        self.destination_directory = destination_directory

    def get_full_path(self, offset: int = None):
        """
        :return: Returns the full path that will join all fields according to the following format if no offset if provided:
        'destination_directory'/'symbol_class'/'raw_file_name_without_extension'_'stroke_thickness'.'extension',
        e.g.: data/images/3-4-Time/1-13_3.png

        or with an additional offset-appendix if an offset is provided
        'destination_directory'/'symbol_class'/'raw_file_name_without_extension'_'stroke_thickness'_offset_'offset'.'extension',
        e.g.: data/images/3-4-Time/1-13_3_offset_74.png
        """
        if offset is None:
            return os.path.join(self.destination_directory, self.symbol_class,
                                "{0}_{1}.{2}".format(self.raw_file_name_without_extension, self.stroke_thickness,
                                                     self.extension))
        else:
            return os.path.join(self.destination_directory, self.symbol_class,
                                "{0}_{1}_offset_{2}.{3}".format(self.raw_file_name_without_extension,
                                                                self.stroke_thickness, offset, self.extension))

    def get_class_name_and_file_path(self, offset: int = None):
        if offset is None:
            return os.path.join(self.symbol_class,
                                "{0}_{1}.{2}".format(self.raw_file_name_without_extension, self.stroke_thickness,
                                                     self.extension))
        else:
            return os.path.join(self.symbol_class, "{0}_{1}_offset_{2}.{3}".format(self.raw_file_name_without_extension,
                                                                                   self.stroke_thickness, offset,
                                                                                   self.extension))
