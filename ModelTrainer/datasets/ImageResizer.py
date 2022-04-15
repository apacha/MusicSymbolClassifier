import os
from glob import glob
from itertools import repeat

from PIL import Image
from tqdm.contrib.concurrent import process_map


class ImageResizer:
    def resize_all_images(self, image_dataset_directory: str, width: int, height: int, resampling_mode: int) -> None:
        """
        Resizes all *.png images in a directory in-situ to the specified width and height with the desired resampling
        method.

        :param image_dataset_directory:
        :param width: The desired width of the images to be resized to
        :param height: The desired height of the images to be resized to
        :param resampling_mode: The resampling method to be used.
            See :py:meth:`~PIL.Image.Image.resize` in :py:class:`PIL.Image.Image` for more details.
        """
        all_images = [y for x in os.walk(image_dataset_directory) for y in glob(os.path.join(x[0], '*.png'))]
        process_map(
            self.resize_image,
            all_images,
            repeat(width),
            repeat(height),
            repeat(resampling_mode),
            max_workers=os.cpu_count(),
            desc="Resizing all images"
        )

    def resize_image(self, image_path: str, width: int, height: int, resampling_mode: int):
        img = Image.open(image_path).convert('RGB')
        hw_tuple = (height, width)
        if img.size != hw_tuple:
            img = img.resize(hw_tuple, resampling_mode)
            img.save(image_path)


if __name__ == "__main__":
    image_resizer = ImageResizer()
    image_resizer.resize_all_images("../data/images", 96, 96, Image.LANCZOS)
