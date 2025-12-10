"""
Main script - connects all components into a pipeline
"""
import argparse
import multiprocessing
from multiprocessing import Queue, Process
import cv2

from streamer import streamer_process
from detector import detector_process
from displayer import displayer_process


def main():
    parser = argparse.ArgumentParser(description='Video motion detection system')
    parser.add_argument('-v', '--video', type=str, required=True,
                       help='Path to video file')
    parser.add_argument('-a', '--min-area', type=int, default=100,
                       help='Minimum area for motion detection (default: 100)')
    
    args = parser.parse_args()
    
    # Limit queue size to prevent memory buildup if processing is slower than streaming
    streamer_to_detector = Queue(maxsize=10)
    detector_to_displayer = Queue(maxsize=10)
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {args.video}")
        return
    
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0:
        video_fps = 30
    cap.release()
    
    print(f"Starting motion detection system")

    
    processes = []
    
    p_streamer = Process(target=streamer_process, 
                        args=(args.video, streamer_to_detector, video_fps))
    p_streamer.start()
    processes.append(p_streamer)
    
    p_detector = Process(target=detector_process,
                        args=(streamer_to_detector, detector_to_displayer, args.min_area))
    p_detector.start()
    processes.append(p_detector)
    
    p_displayer = Process(target=displayer_process,
                         args=(detector_to_displayer, video_fps))
    p_displayer.start()
    processes.append(p_displayer)
    
    try:
        for p in processes:
            p.join()
            
    except KeyboardInterrupt:
        print("\nReceived Ctrl+C - terminating system...")
        for p in processes:
            p.terminate()
            p.join(timeout=2)
            if p.is_alive():
                p.kill()
    
    print("System finished")


if __name__ == "__main__":
    main()

