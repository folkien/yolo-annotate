#!/usr/bin/python3
import cv2
import numpy as np
import logging
import argparse
import sys
import engine.annote as annote
from engine.gui import *
from engine.annoter import *
from helpers.files import *
from helpers.textAnnotations import *
from ObjectDetectors.DetectorYOLOv4COCO import DetectorYOLOv4COCO
from ObjectDetectors.DetectorYOLOv4custom import DetectorYOLOv4custom

# Arguments and config
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Input path')
parser.add_argument('-c', '--config', type=str,
                    required=False, help='Config path')
parser.add_argument('-oc', '--onlyClass', type=int,
                    required=False, help='Only specific class number')
parser.add_argument('-on', '--onlyNewFiles', action='store_true',
                    required=False, help='Process only files without detections file.')
parser.add_argument('-oe', '--onlyFilesWithErrors', action='store_true',
                    required=False, help='Process only files with errors.')
parser.add_argument('-yc', '--yoloCustom', action='store_true',
                    required=False, help='Use custom YOLO.')
parser.add_argument('-v', '--verbose', action='store_true',
                    required=False, help='Show verbose finded and processed data')
args = parser.parse_args()

# Check - input argument
if (args.input is None):
    print('Error! No arguments!')
    sys.exit(-1)

# Check - files filter
isOnlyNewFiles = False
if (args.onlyNewFiles):
    isOnlyNewFiles = True

# Check - files filter
isOnlyErrorFiles = False
if (args.onlyFilesWithErrors):
    isOnlyErrorFiles = True

# Check - files filter
isOnlySpecificClass = None
if (args.onlyClass is not None):
    isOnlySpecificClass = args.onlyClass

# Enabled logging
if (__debug__ is True):
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.debug('Logging enabled!')

# Create detector
if (args.yoloCustom):
    detector = DetectorYOLOv4custom()
else:
    detector = DetectorYOLOv4COCO()
annote.Init(detector.GetClassNames())

# Create annoter
annoter = Annoter(args.input, detector, isOnlyNewFiles,
                  isOnlyErrorFiles, isOnlySpecificClass)

# Start Gui
g = Gui('YoloAnnotate')
g.SetAnnoter(annoter)
g.Start()
