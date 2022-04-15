from pathlib import Path
import shutil
from os import listdir
import configs
from time import sleep


def move_files(source_folder, dest_folder):
    Files_to_move = listdir(source_folder)

    for file in Files_to_move:
        shutil.move( f"{source_folder}/{file}", f"{dest_folder}/{file}")
        sleep(1)