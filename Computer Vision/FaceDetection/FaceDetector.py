import cv2
import glob
import os
import json
import sys

def detect_faces(cascade, image, scaleFactor = 1.1, minNeighbors = 5):
    # Make a copy and convert to grayscale to apply the detection.
    image_copy = image.copy()
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    faces_rect = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    return faces_rect

try:
    image_dir = sys.argv[1]
except IndexError:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(dir_path, r'Test folder/images/')

output_dir = os.path.join(image_dir, r'results.json')

haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
image_paths = glob.glob(os.path.join(image_dir, "*.jpg"))
output_list = []

for image_path in image_paths:
    _, filename = os.path.split(image_path)
    image = cv2.imread(image_path)
    results = detect_faces(haar_cascade, image)
    for result in results:
        output_list.append({"iname": filename, "bbox": list(map(int, result))})
    # Draw Rectangles on the images.
    # for (x, y, w, h) in results:
    #     cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Writing the results to json file.
with open(output_dir, 'w') as f:
    json.dump(output_list, f, indent=4)
with open(r'results.json', 'w') as f:
    json.dump(output_list, f, indent=4)


# !python /content/drive/MyDrive/openCV/Project3_FaceDetection/ComputeFBeta/ComputeFBeta.py results.json ground-truth.json
