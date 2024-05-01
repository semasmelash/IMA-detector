from ultralytics import YOLO
import yaml
import os

data_dict = {
    'names': ['IMA'],
    'train': 'datasets/images/train',
    'val': 'datasets/images/val'
}

with open('data.yaml', 'w') as yaml_file:
    yaml.dump(data_dict, yaml_file)

yolo = YOLO('yolov8n-obb.pt')
yolo.train(data='data.yaml', epochs=5)
valid_results = yolo.val()

