import argparse
import os

from DatasetDownloader import DatasetDownloader


def create_images():

    destination_file = "HOMUS.zip"
    if not os.path.exists(destination_file):
        dataset_downloader = DatasetDownloader()
        dataset_downloader.download_file("http://grfia.dlsi.ua.es/homus/HOMUS.zip")

    pass



if __name__ == "__main__":

    create_images()
