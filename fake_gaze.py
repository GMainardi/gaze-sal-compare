import numpy as np
import cv2 as cv

class FakeGaze:

    def __init__(self, radius: int) -> None:
        self.radius = radius

    def __dist_from_center(self, x, y) -> float:
        return np.sqrt((x-self.radius)**2 + (y-self.radius)**2) / self.radius
    
    def __fill_circle(self, image: np.array) -> np.array:
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                dist = self.__dist_from_center(x, y)

                if abs(dist) > 1:
                    continue
            
                color =  int(255 * (1 - dist))
                image[x, y] = (0, 0, color) #tuple([color]*3)

    def create_circle(self) -> np.array:
        image = np.zeros((self.radius*2, self.radius*2, 3), np.uint8)
        self.__fill_circle(image)
        return image
    
    def create_gaze_image(self, shape, center) -> np.array:
        image = np.zeros(shape, np.uint8)
        filled_image = self.create_circle()

        slice = image[center[1]-self.radius:center[1]+self.radius, 
                center[0]-self.radius:center[0]+self.radius]
        
        filled_image = cv.resize(filled_image, slice.shape[:2][::-1])

        image[center[1]-self.radius:center[1]+self.radius, 
                center[0]-self.radius:center[0]+self.radius] = filled_image
        return image