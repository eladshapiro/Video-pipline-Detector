# Video Motion Detection System

This system performs analytics on video streams using a pipeline architecture consisting of three independent components.

## Architecture

The system is built from three separate components, each running as an independent process:

1. **Streamer** (`streamer.py`) - Reads video and sends frames to the next component
2. **Detector** (`detector.py`) - Detects motion in images and sends image + detections
3. **Displayer** (`displayer.py`) - Applies Gaussian blur to detected motion areas, draws bounding boxes, adds timestamp, and displays on screen

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
python main.py -v "People - 6387.mp4" 
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
3. **Displayer**: Receives image + detections, applies Gaussian blur to detected motion areas , draws green rectangles around motion areas, adds timestamp in the top-left corner, and displays the video

## Data Flow

The system processes video data through a pipeline architecture:

```
Video File
    ↓
[Streamer Process]
    ↓ (frame_num, frame) → Queue1 (maxsize=10)
[Detector Process]
    ↓ (frame_num, frame.copy(), detections) → Queue2 (maxsize=10)
[Displayer Process]
    ↓
Display Window (with blurred motion areas, bounding boxes, and timestamp)
```

### Data Format Between Components:

- **Streamer → Detector**: `(frame_count: int, frame: numpy.ndarray)`
- **Detector → Displayer**: `(frame_num: int, frame: numpy.ndarray, detections: list)`
  - Each detection: `{'x': int, 'y': int, 'w': int, 'h': int, 'area': float}`
- **Termination Signal**: `None` sent through queues to signal end of processing

## Design Principles

The system follows several key design principles:

1. **Separation of Concerns**: Each component has a single, well-defined responsibility
   - Streamer: Video I/O only
   - Detector: Motion detection algorithm only
   - Displayer: Visualization only

2. **Inter-Process Communication**: Uses `multiprocessing.Queue` with `maxsize=10` to prevent memory buildup if processing is slower than streaming

3. **Synchronization**: Uses `None` as a termination signal passed through queues to gracefully shut down all processes

4. **Performance**: Parallel processing of three independent processes allows for better CPU utilization

5. **Memory Management**: 
   - Detector sends `frame.copy()` to avoid modifying the original frame
   - Queue size limits prevent unbounded memory growth
   - Each process manages its own resources independently

6. **Error Handling**: Each component has try-except blocks and proper cleanup in finally blocks

7. **Graceful Shutdown**: Handles KeyboardInterrupt (Ctrl+C) to cleanly terminate all processes

## Important Notes

- Only the **Displayer** component modifies the image - the Detector sends a clean image + detection information
- The Displayer applies **Gaussian blur** to detected motion areas 
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
