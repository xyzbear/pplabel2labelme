import json
import base64
from PIL import Image
import io
import os
import cv2
import numpy as np

def generate_json(txt_file_path, img_file_path):
    str_json = {}
    shapes = []

    with open(txt_file_path, 'r') as file:
        data = json.load(file)

        for shape_data in data:
            transcription = shape_data["transcription"]
            points = shape_data["points"]

            shape_points = [[float(point[0]), float(point[1])] for point in points]

            shape = {
                "label": transcription,
                "points": shape_points,
                "line_color": [],
                "fill_color": [],
                "flags": {}
            }
            shapes.append(shape)

    str_json["version"] = "3.14.1"
    str_json["flags"] = {}
    str_json["shapes"] = shapes
    str_json["lineColor"] = [0, 255, 0, 128]
    str_json["fillColor"] = [255, 0, 0, 128]

    str_json["imagePath"] = os.path.basename(img_file_path)
    img = cv2.imread(img_file_path)
    str_json["imageHeight"] = img.shape[0]
    str_json["imageWidth"] = img.shape[1]
    str_json["imageData"] = base64encode_img(img_file_path)

    return str_json

def base64encode_img(image_path):
    src_image = Image.open(image_path)
    output_buffer = io.BytesIO()
    src_image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str

if __name__ == "__main__":
    # 替换为文件夹路径
    folder_path = "../do_lables/txt"

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('txt'):
            txt_file_path = os.path.join(folder_path, file_name)
            img_file_path = os.path.join(folder_path, file_name.replace('.txt', '.png'))

            str_json = generate_json(txt_file_path, img_file_path)
            json_data = json.dumps(str_json, indent=2, ensure_ascii=False)

            jsonfile_name = file_name.replace(".txt", ".json")
            with open(os.path.join(folder_path, jsonfile_name), 'w') as f:
                f.write(json_data)