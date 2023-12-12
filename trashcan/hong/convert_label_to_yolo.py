import os
import glob
from utils.labelme2yolo import convert
from tqdm import tqdm

def convert_folder(folder_path):
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    for file in tqdm(json_files):
        convert(file)

convert_folder("./json")
# convert_folder("../../ref/aihub/data/train/label_west_indoor")