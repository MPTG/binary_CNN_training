import cv2

class VideoROISelector:
    """
    Class representing a video ROI selector. Enable choose the correct ROI
    """
    def __init__(self, video_path):
        self.video_path = video_path
        self.roi = None

    def get_roi(self):
        cap = cv2.VideoCapture(self.video_path)

        if not(cap.isOpened()):
            raise IOError("Could not open video file")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise IOError("Could not read first video frame")

        self.roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()

        x, y, w, h = self.roi
        return x, y, w, h

