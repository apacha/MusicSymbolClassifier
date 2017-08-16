import os
from glob import glob

import sys
from PIL import Image
from tqdm import tqdm


class ImageResizer:
    def resize_all_images(self, image_dataset_directory, width, height, resampling_mode):
        all_images = [y for x in os.walk(image_dataset_directory) for y in glob(os.path.join(x[0], '*.png'))]
        for image_path in tqdm(all_images, desc="Resizing images", smoothing=0.1, mininterval=0.25):
            img = Image.open(image_path).convert('RGB')
            hw_tuple = (height, width)
            if img.size != hw_tuple:
                img = img.resize(hw_tuple, resampling_mode)
                img.save(image_path)


if __name__ == "__main__":
    image_resizer = ImageResizer()
    image_resizer.resize_all_images("../data/images", 96, 96, Image.LANCZOS)
