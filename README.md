# Video Motion Detection System

This system performs analytics on video streams using a pipeline architecture consisting of three independent components.

## Architecture

The system is built from three separate components, each running as an independent process:

1. **Streamer** (`streamer.py`) - Reads video and sends frames to the next component
2. **Detector** (`detector.py`) - Detects motion in images and sends image + detections
3. **Displayer** (`displayer.py`) - Draws detections on the image, adds timestamp, and displays on screen

## Inter-Component Communication

Communication between processes is done using **multiprocessing.Queue**:
- **Advantages**: Easy to use, thread-safe, supports large data (images), suitable for continuous data flow
- **Decision**: I chose Queue because it's the simplest and most reliable solution for inter-process communication in Python, especially for video data

## Requirements

```bash
pip install opencv-python imutils
```

## Usage

```bash
python main.py -v "People - 6387.mp4" -a 100
```

### Parameters:
- `-v, --video`: Path to video file (required)
- `-a, --min-area`: Minimum area for motion detection (default: 100)

### Example:
```bash
python main.py -v "People - 6387.mp4"
```

## How It Works

1. **Streamer**: Reads the video frame by frame and sends each frame to the Queue
2. **Detector**: Receives frames, compares each frame to the previous one, detects motion areas, and sends the original image + list of detections (bounding boxes)
3. **Displayer**: Receives image + detections, draws green rectangles around motion areas, adds timestamp in the top-left corner, and displays the video

## Important Notes

- Only the **Displayer** component draws on the image - the Detector sends a clean image + detection information
- The system maintains the original video rate through FPS control in the Displayer component
- Pressing 'q' will close the window and terminate the system

## File Structure

```
.
├── main.py          # Main script - connects all components
├── streamer.py      # Streamer component
├── detector.py      # Detector component
├── displayer.py    # Displayer component
└── README.md        # This file
```
