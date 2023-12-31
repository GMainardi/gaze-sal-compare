from enum import Enum
import cv2 as cv
import numpy as np

from heatmap_extractor import HeatmapCenterExtractor
from fake_gaze import FakeGaze

class Mode(Enum):
    SCREEN= 1
    HEATMAP = 2
    SALIENCY = 3
    HEATMAP_SALIENCY = 4

class ImageProcessor:

    def __init__(self, 
        screen_images: list[np.array], 
        heatmap_images: list[np.array], 
        saliency_images: list[np.array]
    ) -> None:
        
        self.screen_images = screen_images
        self.heatmap_images = heatmap_images
        self.saliency_images = saliency_images
        self.index = 0
        self.mode =  Mode.SCREEN
        self.heatmap_center_extractor = HeatmapCenterExtractor()
    
    def __merge_frames(self, screen: np.array, mask: np.array) -> np.array:
        return cv.addWeighted(screen, 0.5, mask, 0.8, 0)
    
    def __get_heatmap_detection(self, screen: np.array, heatmap: np.array):

        diff = cv.absdiff(cv.cvtColor(screen, cv.COLOR_BGR2GRAY),
                        cv.cvtColor(heatmap, cv.COLOR_BGR2GRAY))
        
        _, bi = cv.threshold(diff,15,255,0)

        circle = self.heatmap_center_extractor.get_saliency_contour(bi)
        return (int(circle[0][0]), int(circle[0][1])), int(circle[1])

    def _dim_circle(self, radius: int) -> np.array:
        '''
        creates an image of a circle with value (255, 255, 255) on center and getting gradualy darker on borders
        '''
        image = np.zeros((radius*2, radius*2, 3), np.uint8)

        image[radius, radius] = (255, 255, 255)

    def __get_blue_saliency(self, saliency: np.array) -> np.array:
        saliency = cv.cvtColor(saliency, cv.COLOR_GRAY2BGR)
        saliency[:, :, 1] = 0
        saliency[:, :, 2] = 0
        return saliency
    
    def __get_purple_saliency(self, saliency: np.array) -> np.array:
        saliency = cv.cvtColor(saliency, cv.COLOR_GRAY2BGR)
        saliency[:, :, 1] = 0
        return saliency
    
    def __get_gaze_saliency(self, screen: np.array, heatmap: np.array) -> np.array:
        center, radius = self.__get_heatmap_detection(screen, heatmap)
        fake_gaze = FakeGaze(radius)
        return fake_gaze.create_gaze_image(screen.shape, center)
    
    def get_image(self) -> np.array:
        
        match self.mode:
            case Mode.SCREEN: # screen only
                return self.screen
            case Mode.HEATMAP: # gaze data
                return self.__merge_frames(self.screen, 
                                           self.__get_gaze_saliency(self.screen, self.heatmap))   

            case Mode.SALIENCY:
                return self.__merge_frames(self.screen, 
                                           self.__get_blue_saliency(self.saliency))
            case Mode.HEATMAP_SALIENCY:
                
                gray_heatmap = cv.cvtColor(self.__get_gaze_saliency(self.screen, self.heatmap), cv.COLOR_BGR2GRAY)
                mask = (gray_heatmap/25 * self.saliency) 
                mask[mask > 255] = 255
                return self.__merge_frames(self.screen, self.__get_purple_saliency(mask.astype(np.uint8)))
    
    @property
    def next(self) -> None:
        self.index = min(self.index + 1, len(self.screen_images) - 1)

    @property
    def prev(self) -> None:
        self.index = max(self.index - 1, 0)

    @property
    def saliency_on(self) -> None:
        if self.mode == Mode.SCREEN:
            self.mode = Mode.SALIENCY
        elif self.mode == Mode.HEATMAP:
            self.mode = Mode.HEATMAP_SALIENCY
    
    @property
    def saliency_off(self) -> None:
        if self.mode == Mode.SALIENCY:
            self.mode = Mode.SCREEN
        elif self.mode == Mode.HEATMAP_SALIENCY:
            self.mode = Mode.HEATMAP

    @property
    def heatmap_on(self) -> None:
        if self.mode == Mode.SCREEN:
            self.mode = Mode.HEATMAP
        elif self.mode == Mode.SALIENCY:
            self.mode = Mode.HEATMAP_SALIENCY
    
    @property
    def heatmap_off(self) -> None:
        if self.mode == Mode.HEATMAP:
            self.mode = Mode.SCREEN
        elif self.mode == Mode.HEATMAP_SALIENCY:
            self.mode = Mode.SALIENCY

    @property
    def screen(self) -> np.array:
        return cv.imread(self.screen_images[self.index])
    
    @property
    def heatmap(self) -> np.array:
        return cv.imread(self.heatmap_images[self.index])
    
    @property
    def saliency(self) -> np.array:
        return cv.imread(self.saliency_images[self.index], cv.IMREAD_GRAYSCALE)
    