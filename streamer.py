"""
Streamer component - reads video and sends frames to the detector component
"""
import cv2
from multiprocessing import Process, Queue


def streamer_process(video_path, output_queue, fps=None):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return
    
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                # Send None as termination signal to downstream processes
                output_queue.put(None)
                break
            
            output_queue.put((frame_count, frame))
            frame_count += 1
            
    except Exception as e:
        print(f"Error in streamer: {e}")
    finally:
        cap.release()
        print("Streamer: Finished reading video")


if __name__ == "__main__":
    test_queue = Queue()
    streamer_process("People - 6387.mp4", test_queue)

