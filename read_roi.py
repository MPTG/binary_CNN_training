from libraries.read_ROI_values import VideoROISelector
from libraries.read_config import ReadConfig

def read_roi() -> None:
    config_path = 'data/config.json'
    config = ReadConfig(config_path)
    config = config.read_config()
    video = VideoROISelector(config['video_path'])
    x, y, w, h = video.get_roi()
    print(x, y, w, h)

read_roi()

