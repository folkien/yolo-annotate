#!/usr/bin/python3
import cv2
import numpy as np
import logging
import argparse
import sys
import engine.annote as annote
from engine.gui import *
from helpers.files import *
from helpers.textAnnotations import *
from ObjectDetectors.DetectorYOLOv4COCO import DetectorYOLOv4COCO
from ObjectDetectors.DetectorYOLOv4custom import DetectorYOLOv4custom

# Arguments and config
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Input path')
parser.add_argument('-on', '--onlyNewFiles', action='store_true',
                    required=False, help='Process only files without detections file.')
parser.add_argument('-yc', '--yoloCustom', action='store_true',
                    required=False, help='Use custom YOLO.')
parser.add_argument('-v', '--verbose', action='store_true',
                    required=False, help='Show verbose finded and processed data')
args = parser.parse_args()

if (args.input is None):
    print('Error! No arguments!')
    sys.exit(-1)

# Enabled logging
if (__debug__ is True):
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.debug('Logging enabled!')

excludes = ['.', '..', './', '.directory']
dirpath = args.input
filenames = os.listdir(dirpath)
# Create detector
if (args.yoloCustom):
    detector = DetectorYOLOv4custom()
else:
    detector = DetectorYOLOv4COCO()
annote.Init(detector.GetClassNames())

# Step 0 - filter only images
filenames = [f for f in filenames if (f not in excludes) and (IsImageFile(f))]

# Step 1 - process all images
for f in filenames:
    # Read image
    im = cv2.imread(dirpath+f)
    height, width = im.shape[0:2]

    # If exists annotations file
    if (IsExistsAnnotations(dirpath+f)):
        annotations = ReadAnnotations(dirpath+f)
        annotations = [annote.fromTxtAnnote(el) for el in annotations]
    # else detect by YOLO
    else:
        annotations = detector.Detect(im, boxRelative=True)
        annotations = [annote.fromDetection(el) for el in annotations]

    # Start Gui
    g = Gui('YoloAnnotate', im)
    g.SetAnnotations(annotations)
    g.Start()
