import os
from argparse import ArgumentParser

import numpy
from PIL import Image
from scipy import ndimage
from skimage.transform import resize


def copy_and_resize(image_directory: str, target_directory: str, rescaled_width: int = 128, rescaled_height: int = 128):
    os.makedirs(target_directory, exist_ok=True)
    for image_class in ["other", "scores"]:
        index = 0
        image_class_directory = os.path.join(image_directory, image_class)
        class_target_directory = os.path.join(target_directory, image_class)
        os.makedirs(class_target_directory, exist_ok=True)
        for file in os.listdir(image_class_directory):
            # print(file)
            image = ndimage.imread(os.path.join(image_class_directory, file))
            if image.ndim == 3:
                output_shape = (rescaled_width, rescaled_height, 3)
            else:
                output_shape = (rescaled_width, rescaled_height)

            resized = resize(image, output_shape=output_shape, preserve_range=True)
            destination_file_name = os.path.join(class_target_directory, image_class + "_" + str(index) + ".png")
            resized_image = Image.fromarray(resized.astype(numpy.uint8))
            resized_image.save(destination_file_name)
            index += 1

def rename_all_files_in_directory():
    folder = "C:\\Users\\Alex\\Dropbox\\Doktorat\\MusicScoresDataset\\other"
    i = 0
    prefix = "other_"
    for file in os.listdir(folder):
        extension = file[-4:]
        target_name = prefix + str(i) + extension
        print ("renaming {0} to {1}".format(file, target_name))
        os.rename(os.path.join(folder, file), os.path.join(folder, target_name))
        i += 1

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--image_directory",
        dest="image_directory",
        type=str,
        default="C:\\Users\\Alex\\Repositories\\MusicScoreClassifier\\ModelGenerator\\data",
        help="The directory that contains the entire image dataset (including two subfolders called other and scores for the two classes.",
    )
    parser.add_argument(
        "-t",
        "--target_directory",
        dest="target_directory",
        type=str,
        default="C:\\Users\\Alex\\Repositories\\MusicScoreClassifier\\ModelGenerator\\data\\entire_dataset_128x128",
        help="The destination folder into which all files should be copied to",
    )

    args = parser.parse_args()
    # if len(sys.argv) < 3:
    #     parser.print_help()
    #     exit(-1)

    copy_and_resize(args.image_directory, args.target_directory)

