'''
Created on 17 lis 2020

@author: spasz
'''
import os
import cv2
import logging
import engine.annote as annote
from helpers.files import IsImageFile
from helpers.textAnnotations import ReadAnnotations, SaveAnnotations, IsExistsAnnotations


class Annoter():
    '''
    classdocs
    '''

    def __init__(self, filepath, detector):
        '''
        Constructor
        '''
        self.detector = detector
        self.dirpath = filepath

        # filter only images and not excludes
        excludes = ['.', '..', './', '.directory']
        filenames = os.listdir(self.dirpath)
        self.filenames = [f for f in filenames if (
            f not in excludes) and (IsImageFile(f))]

        # Current file number offset
        self.offset = 0
        self.image = None
        self.annotations = None

    def __getFilename(self):
        ''' Returns current filepath.'''
        return self.filenames[self.offset]

    def GetImage(self):
        ''' Returns current image.'''
        return self.image

    def GetImageNumber(self):
        ''' Returns current image number.'''
        return self.offset

    def GetImagesCount(self):
        ''' Returns count of processed images number.'''
        return len(self.filenames)

    def SetImageNumber(self, number):
        ''' Sets current image number.'''
        if (number >= 0) and (number < len(self.filenames)):
            self.offset = number
            self.Process()
            return True

        return False

    def GetAnnotations(self):
        ''' Returns current annotations.'''
        return self.annotations

    def AddAnnotation(self, box, classNumber):
        ''' Adds new annotation by human.'''
        self.annotations.append(annote.Annote(
            box, classNumber=classNumber, authorType=annote.AnnoteAuthorType.byHand))
        logging.debug('(Annoter) Added annotation class %u!', classNumber)

    def ClearAnnotations(self):
        ''' Clear all annotations.'''
        self.annotations = []
        logging.debug('(Annoter) Cleared annotations!')

    def Save(self):
        ''' Save current annotations.'''
        annotations = [annote.toTxtAnnote(el) for el in self.annotations]
        annotations = SaveAnnotations(
            self.dirpath+self.__getFilename(), annotations)
        logging.debug('(Annoter) Saved annotations for %s!',
                      self.__getFilename())
        # Process file again after save
        self.Process()

    def IsEnd(self):
        '''True if files ended.'''
        return (self.offset == len(self.filenames))

    def Process(self):
        ''' process file.'''
        if (self.offset >= 0) and (self.offset < len(self.filenames)):
            f = self.__getFilename()

            # Read image
            im = cv2.imread(self.dirpath+f)

            annotations = []
            # If exists annotations file
            if (IsExistsAnnotations(self.dirpath+f)):
                annotations = ReadAnnotations(self.dirpath+f)
                annotations = [annote.fromTxtAnnote(el) for el in annotations]
                logging.debug(
                    '(Annoter) Loaded annotations from %s!', self.dirpath+f)
            # if annotations file not exists or empty then detect.
            if (len(annotations) == 0):
                annotations = self.detector.Detect(
                    im, confidence=0.3, boxRelative=True)
                annotations = [annote.fromDetection(el) for el in annotations]
                logging.debug(
                    '(Annoter) Detected annotations for %s!', self.dirpath+f)

            self.image = im
            self.annotations = annotations
            return True

        return False

    def ProcessNext(self):
        ''' Process next image.'''
        if (self.offset < (len(self.filenames)-1)):
            self.offset += 1
            self.Process()
            return True

        return False

    def ProcessPrev(self):
        ''' Process next image.'''
        if (self.offset > 0):
            self.offset -= 1
            self.Process()
            return True

        return False
