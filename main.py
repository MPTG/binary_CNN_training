from libraries.read_ROI_values import VideoROISelector

def main() -> None:
    video_path = 'data/0%.mp4'
    video = VideoROISelector(video_path)
    x, y, w, h = video.get_roi()
    print(x, y, w, h)

if __name__ == "__main__":
    main()