import os
from glob import glob

import sys
from PIL import Image


class ImageResizer:
    def resize_all_images(self, image_dataset_directory, width, height, resampling_mode):
        all_images = [y for x in os.walk(image_dataset_directory) for y in glob(os.path.join(x[0], '*.png'))]
        image_counter = 1
        number_of_images = len(all_images)
        for image_path in all_images:
            self.__write_progress("Resizing images {0: >5} of {1}".format(image_counter, number_of_images))
            image_counter += 1
            img = Image.open(image_path).convert('RGB')
            hw_tuple = (height, width)
            if img.size != hw_tuple:
                img = img.resize(hw_tuple, resampling_mode)
                img.save(image_path)

    def __write_progress(self, progress: str):
        sys.stdout.write('\r')
        sys.stdout.write(progress)
        sys.stdout.flush()

if __name__ == "__main__":
    image_resizer = ImageResizer()
    image_resizer.resize_all_images("../temp/2-4-Time", 96, 96, Image.NEAREST)
    image_resizer.resize_all_images("../temp/3-4-Time", 96, 96, Image.BICUBIC)
    image_resizer.resize_all_images("../temp/4-4-Time", 96, 96, Image.BILINEAR)
    image_resizer.resize_all_images("../temp/12-8-Time", 96, 96, Image.LANCZOS)
