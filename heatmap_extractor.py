import cv2

class Detection():

    def __init__(self, contour) -> None:
        self.contour = contour


    @property
    def area(self) -> float:
        return cv2.contourArea(self.contour)
    
    @property
    def center(self) -> tuple[int]:
        x, y, w, h = cv2.boundingRect(self.contour)
        return x + w//2, y + h//2 
    
    @property
    def aprox_vertices(self) -> int:
        return len(self.__aprox())
    
    def __aprox(self) -> any:
        return cv2.approxPolyDP(self.contour,
                                0.01 * cv2.arcLength(self.contour,
                                                    True),
                                True)
    
    @property
    def circle(self) -> tuple[int]:
        return cv2.minEnclosingCircle(self.contour)
    
class HeatmapCenterExtractor():

    def __init__(self) -> None:
        pass
    
    def get_salience_center(self, image):
        return self.get_salience_contour(image).center
    

    def get_salience_contour(self, image):
        contours = self.__get_image_contours(image)
        if len(contours):
            return max(contours, key=lambda x: x.area).circle
        
    def __get_image_contours(self, binary_image: cv2.Mat):
        # Apply HoughCircles transform to detect circles
        contours, _ = cv2.findContours(binary_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        return self.__filter_contours(contours)
    
    def __filter_contours(self, contours):
        return list(map(lambda x: Detection(x), contours))
