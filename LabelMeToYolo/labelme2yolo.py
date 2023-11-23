import os
import json
import base64
import io
import numpy as np
from PIL import Image
import re
import argparse

def read_name_file(name_path):
    with open(name_path, "r", encoding="utf-8") as name_file:
        # names = [name.strip() for name in name_file]
        names = {name.strip(): i  for i, name in enumerate(name_file)}
        
    return names

def convert_coor(size, xy):
    dw, dh = size
    x, y = xy
    return x / dw, y / dh

def convert(file, txt_name=None):
    # print(file)
    if txt_name is None:
        folder, txt_name = file.rstrip(".json").rsplit("/", 1)
        txt_name = os.path.join(folder + "/output/" + txt_name + ".txt")
        
        if not os.path.exists(os.path.dirname(txt_name)):
            os.makedirs(os.path.dirname(txt_name))
            

    names = read_name_file('classes.txt')
    # with open(file, 'r', encoding="utf-8") as f:
    #     Image.fromarray(img_b64_to_arr(json.loads(f.read())['imageData'])).save(txt_name.replace('txt', 'png'))
    
    with open(file, "r", encoding="utf-8") as json_file:
        js = json.loads(json_file.read())

        with open(txt_name, "w", encoding="utf-8") as txt_outfile:
                
            height, width = js["imageHeight"], js["imageWidth"]

            for item in js["shapes"]:
                if len(item["points"]) == 0:
                    continue
                
                label = item["group_id"]
                shape_type = item["shape_type"]

                if shape_type == "polygon":
                    points = item["points"]
                    if len(points) <= 0 :
                        continue

                    txt_outfile.write(str(label))

                    for point in points:
                        x, y = point

                        txt_outfile.write(" " + str(x) + " " + str(y))
                    
                    txt_outfile.write("\n")
                    

def img_data_to_pil(img_data):
    f = io.BytesIO()
    f.write(img_data)
    return Image.open(f)

def img_data_to_arr(img_data):
    return np.array(img_data_to_pil(img_data))

def img_b64_to_arr(img_b64):
    return img_data_to_arr(base64.b64decode(img_b64))

def main():
    print(read_name_file("classes.txt"))
    # convert("train_sample1_out0003.json")
    # parser = argparse.ArgumentParser(description="Convert JSON to TXT")
    # parser.add_argument('--input', type=str, help="Path to the input JSON file", required=True)
    # parser.add_argument('--output', type=str, help="Path to the output TXT file", default=None)
    
    # args = parser.parse_args()
    
    # convert(args.input, args.output)

if __name__ == "__main__":
    main()