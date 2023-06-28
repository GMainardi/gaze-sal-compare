import os
import cv2 as cv

from image_processor import ImageProcessor

class DataLoader:

    def __init__(self, root) -> None:
        self.root = root

    def load_videos(self, user: str) -> tuple:

        screen_frames = [os.path.join(self.root, user, "screen", frame) 
                            for frame in sorted(os.listdir(os.path.join(self.root, user, 'screen')))
                                if frame != '.DS_Store']
        
        hm_frames = [os.path.join(self.root, user, "heatmap", frame) 
                            for frame in sorted(os.listdir(os.path.join(self.root, user, 'heatmap')))
                                if frame != '.DS_Store']

        sal_frames = [os.path.join(self.root, user, "sal", frame) 
                            for frame in sorted(os.listdir(os.path.join(self.root, user, 'sal')))
                                if frame != '.DS_Store']

        return sorted(screen_frames), sorted(hm_frames), sorted(sal_frames)

    def load_data(self):
        subjects = {}
        for folder in os.listdir(self.root):
            if folder != '.DS_Store':
                screen_frames, hm_frames, sal_frames = self.load_videos(folder)

                subjects[folder] = ImageProcessor(screen_frames, hm_frames, sal_frames)
        return subjects