"""
Displayer component - draws detections on image, adds timestamp, and displays on screen
"""
import cv2
import datetime
import time
from multiprocessing import Process, Queue


def displayer_process(input_queue, fps=None):
    if fps is None:
        fps = 30
    
    frame_time = 1.0 / fps
    
    try:
        while True:
            data = input_queue.get()
            
            if data is None:
                break
            
            frame_num, frame, detections = data
            
            # Draw bounding boxes around detected motion areas
            for det in detections:
                x, y, w, h = det['x'], det['y'], det['w'], det['h']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display current timestamp
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, current_time, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Motion Detection', frame)
            
            # Check for 'q' key press (waitKey returns -1 if no key pressed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Maintain video playback rate
            time.sleep(frame_time)
            
    except Exception as e:
        print(f"Error in displayer: {e}")
    finally:
        cv2.destroyAllWindows()
        print("Displayer: Finished displaying")


if __name__ == "__main__":
    test_queue = Queue()
    displayer_process(test_queue)

