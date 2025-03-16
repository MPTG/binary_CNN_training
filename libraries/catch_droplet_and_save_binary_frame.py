import cv2
import pandas as pd
import numpy as np
import os


class VideoAnalyzer:
    def __init__(self, video_path, roi, output_folder, area_threshold, no_frames) -> None:
        self.video_path = video_path
        self.roi = roi
        self.output_folder = output_folder
        self.area_threshold = area_threshold
        self.no_frames = no_frames
        self.cap = cv2.VideoCapture(self.video_path)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        self.frame_number = 0
        self.saved_frames = 0

        self.particle_data = pd.DataFrame(columns=[
            'Frame', 'Time (ms)', 'Area', 'Perimeter', 'Aspect Ratio',
            'Circularity', 'Convexity', 'Max Height', 'Min Length'
        ])

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def process_frame(self, frame):
        x, y, w, h = self.roi
        timestamp_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)

        # Apply ROI and background subtraction
        frame_roi = frame[y:y + h, x:x + w]
        fgMask = self.backSub.apply(frame_roi)
        blurred = cv2.GaussianBlur(fgMask, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)

        # Create a binary mask
        mask = np.zeros_like(frame_roi, dtype=np.uint8)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected = False

        for contour in contours:
            if self.analyze_contour(contour, timestamp_ms):
                detected = True
                cv2.drawContours(frame_roi, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

        # Save frame if a droplet is detected and the limit is not exceeded
        if detected and self.saved_frames < self.no_frames:
            frame_path = os.path.join(self.output_folder, f"frame_{self.saved_frames:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            self.saved_frames += 1

        cv2.imshow('Particle Detection', frame)

    def analyze_contour(self, contour, timestamp_ms):
        area = cv2.contourArea(contour)
        if area > self.area_threshold:
            perimeter = cv2.arcLength(contour, True)
            x_min, y_min, width, height = cv2.boundingRect(contour)
            max_height, min_length = height, width

            if len(contour) >= 5:
                _, (major_axis, minor_axis), _ = cv2.fitEllipse(contour)
                aspect_ratio = major_axis / minor_axis
                circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                convexity = area / hull_area if hull_area > 0 else 0
                self.particle_data = pd.concat([self.particle_data, pd.DataFrame([{
                    'Frame': self.frame_number,
                    'Time (ms)': timestamp_ms,
                    'Area': area,
                    'Perimeter': perimeter,
                    'Aspect Ratio': aspect_ratio,
                    'Circularity': circularity,
                    'Convexity': convexity,
                    'Max Height': max_height,
                    'Min Length': min_length
                }])], ignore_index=True)
                return True
        return False

    def analyze_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_number += 1
            self.process_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or self.saved_frames >= self.no_frames:
                break

        self.save_results()
        self.cleanup()

    def save_results(self):
        output_excel_path = os.path.join(self.output_folder, "particle_data.xlsx")
        self.particle_data.to_excel(output_excel_path, index=False)
        print(f"All processed frames saved to {self.output_folder}")
        print(f"Particle data saved to {output_excel_path}")

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()