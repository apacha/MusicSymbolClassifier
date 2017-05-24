import argparse
import os
import random
import shutil
import urllib.parse as urlparse
import urllib.request as urllib2
from abc import ABC, abstractmethod
from typing import List
import numpy


class DatasetDownloader:
    """ The abstract base class for the datasets used to train the model """

    def download_file(self, url, destination_filename=None) -> str:
        u = urllib2.urlopen(url)
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)
        if not filename:
            filename = 'downloaded.file'
        if destination_filename:
            filename = destination_filename

        filename = os.path.abspath(filename)

        with open(filename, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
            print("Downloading: {0} Bytes: {1} into {2}".format(url, file_size, filename))

            file_size_dl = 0
            block_sz = 8192
            status_counter = 0
            status_output_interval = 100
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                status += chr(13)
                status_counter += 1
                if status_counter == status_output_interval:
                    status_counter = 0
                    print(status)
                    # print(status, end="", flush=True) Does not work unfortunately
            print()

        return filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        help="The url to the file being downloaded")
    parser.add_argument(
        "--destination_filename",
        type=str,
        default=None,
        help="The destination filename of the file being downloaded (optional)")

    flags, unparsed = parser.parse_known_args()

    datasest = DatasetDownloader()
    datasest.download_file(flags.url, flags.destination_filename)
