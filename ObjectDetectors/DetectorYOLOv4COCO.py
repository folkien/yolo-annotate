'''
Created on 7 lis 2020

@author: spasz
'''
from ObjectDetectors.DetectorYOLOv4 import DetectorYOLOv4


class DetectorYOLOv4COCO(DetectorYOLOv4):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        cfgPath = './ObjectDetectors/yolov4coco/cfg/yolov4.cfg'
        weightPath = './ObjectDetectors/yolov4coco/cfg/yolov4.weights'
        metaPath = './ObjectDetectors/yolov4coco/cfg/coco.data'
        DetectorYOLOv4.__init__(self, cfgPath, weightPath, metaPath)

    def GetAllowedClassNames(self):
        ''' Returns all interesing us class names.'''
        return ['car', 'truck', 'bicycle', 'motorcycle', 'bus']
