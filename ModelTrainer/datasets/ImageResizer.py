import os
from glob import glob

from PIL import Image


class ImageResizer:
    def resize_all_images(self, image_dataset_directory, width, height, resampling_mode):
        all_images = [y for x in os.walk(image_dataset_directory) for y in glob(os.path.join(x[0], '*.png'))]
        for image_path in all_images:
            img = Image.open(image_path).convert('RGB')
            hw_tuple = (height, width)
            if img.size != hw_tuple:
                img = img.resize(hw_tuple, resampling_mode)
                img.save(image_path)


if __name__ == "__main__":
    image_resizer = ImageResizer()
    image_resizer.resize_all_images("../temp/2-4-Time", 96, 96, Image.NEAREST)
    image_resizer.resize_all_images("../temp/3-4-Time", 96, 96, Image.BICUBIC)
    image_resizer.resize_all_images("../temp/4-4-Time", 96, 96, Image.BILINEAR)
    image_resizer.resize_all_images("../temp/12-8-Time", 96, 96, Image.LANCZOS)
