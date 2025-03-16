from libraries.catch_droplet_and_save_binary_frame import VideoAnalyzer
from libraries.read_config import ReadConfig
from libraries.read_ROI_values import VideoROISelector

def main() -> None:
    config_path = 'data/config.json'
    config = ReadConfig(config_path)
    config = config.read_config()
    video = VideoROISelector(config['video_path'])
    roi = video.get_roi()
    analyzer = VideoAnalyzer(
        config['video_path'],
        roi,
        config['output_folder_images'],
        config['treshold'],
        config['no_frames_to_save'])
    analyzer.analyze_video()


if __name__ == "__main__":
    main()