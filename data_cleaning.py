import xml.etree.ElementTree as ET
import math
import shutil
import os

tree = ET.parse('annotations.xml')
root = tree.getroot()

def rotate_point(x, y, cx, cy, angle_rad):

    disp_x = x - cx
    disp_y = y - cy
    rot_x = (disp_x * math.cos(angle_rad) - disp_y * math.sin(angle_rad) + cx)
    rot_y = (disp_x * math.sin(angle_rad) + disp_y * math.cos(angle_rad) + cy)

    return rot_x, rot_y

#tracker to split the images into train, val, and test folders
i = 0

for image in root.findall('image'):

    # Iterate over each box element within the image
    for box in image.findall('box'):

        image_name = image.get('name')

        id = image_name[-8:-4]
        if image_name[16] == 'l':
            image_id = '0' + id + '.jpg'
            label_id = '0' + id + '.txt'
        elif image_name[16] == 'V':
            image_id = '1' + id + '.jpg'
            label_id = '1' + id + '.txt'

        xtl_og = float(box.get('xtl')) / 720
        ytl_og = float(box.get('ytl')) / 480
        xbr_og = float(box.get('xbr')) / 720
        ybr_og = float(box.get('ybr')) / 480
        rotation = float(box.get('rotation', '0'))

        cx = ((xtl_og + xbr_og) / 2)
        cy = (ytl_og + ybr_og) / 2

        angle_rad = math.radians(rotation)

        xbl, ybl = rotate_point(xtl_og, ybr_og, cx, cy, angle_rad)
        xbr, ybr = rotate_point(xbr_og, ybr_og, cx, cy, angle_rad)
        xtl, ytl = rotate_point(xtl_og, ytl_og, cx, cy, angle_rad)
        xtr, ytr = rotate_point(xbr_og, ytl_og, cx, cy, angle_rad)

        if(i < 300):
            image_dir = 'datasets/images/train'
            label_dir = 'datasets/labels/train'
        elif(i < 350):
            image_dir = 'datasets/images/val'
            label_dir = 'datasets/labels/val'
        else:
            image_dir = 'datasets/images/test'
            label_dir = 'datasets/labels/test'
        source_path = image_name
        destination_path = os.path.join(image_dir, image_id)

        shutil.move(source_path, destination_path)

        file_path = os.path.join(label_dir, label_id)

        with open(file_path, 'w') as file:
            file.write(f'0 {xtl} {ytl} {xtr} {ytr} {xbr} {ybr} {xbl} {ybl}')

        i += 1

