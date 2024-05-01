from shapely.geometry import Polygon
import os
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np


yolo = YOLO('runs/obb/train/weights/best.pt')

images_dir = 'datasets/images/test'
labels_dir = 'datasets/labels/test'
images = []
labels = []

for filename in os.listdir(images_dir):
    img_path = os.path.join(images_dir, filename)
    label_path = os.path.join(labels_dir, filename[:-3] + 'txt')
    images.append(img_path)
    labels.append(label_path)

results = yolo.predict(images, save=True, conf=0.3)
predictions = []
zero_box = [(0, 0), (0, 0), (0, 0), (0, 0)]

for result in results:
    obb = result.obb
    num_elms = obb.cls.numel()
    if num_elms == 0:
        predictions.append(zero_box)
    elif num_elms == 1:
        predictions.append(obb.xyxyxyxyn[0].tolist())
    elif num_elms == 2:
        if(obb.conf[0] > obb.conf[1]):
            predictions.append(obb.xyxyxyxyn[0].tolist())
        else:
            predictions.append(obb.xyxyxyxyn[1].tolist())

    elif (num_elms > 2):
        predictions.append(obb.xyxyxyxyn[0].tolist())

true_values = []
for label in labels:
    with open(label) as f:
        line = f.readlines()
        numbers = [float(num) for num in line[0].split()[1:]]
        numbers = np.reshape(numbers, (4, 2)).tolist()
        true_values.append(numbers)

IOU_values = []

for i in range(len(true_values)):

    a = Polygon(predictions[i])
    b = [true_values[i][3], true_values[i][2], true_values[i][1], true_values[i][0]]
    b = Polygon(b)

    if(a.is_valid & b.is_valid):
        IOU = (a.intersection(b).area / a.union(b).area)
        IOU_values.append(IOU)

print(IOU_values)
print(len(true_values))
print(len(IOU_values))

plt.figure(figsize=[10,8])
plt.hist(x=IOU_values, bins=12, color='blue', rwidth=0.85)
plt.xlabel('IOU Value',fontsize=16)
plt.ylabel('Frequency',fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title('IOU Values of Test Images',fontsize=16)
plt.savefig('IOU_graph.jpg')
