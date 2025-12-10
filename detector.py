"""
Detector component - detects motion in images and sends image + detections
"""
import cv2
import imutils
from multiprocessing import Process, Queue


def detector_process(input_queue, output_queue, min_area=100):
    prev_frame = None
    frame_count = 0
    
    try:
        while True:
            data = input_queue.get()
            
            if data is None:
                output_queue.put(None)
                break
            
            frame_num, frame = data
            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
            
            if prev_frame is None:
                # First frame becomes the background reference
                prev_frame = gray_frame
                frame_count += 1
                continue
            
            # Frame differencing: detect changes between consecutive frames
            diff = cv2.absdiff(gray_frame, prev_frame)
            thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)[1]
            
            # Morphological operations: erosion removes noise, dilation fills gaps
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            thresh = cv2.erode(thresh, kernel, iterations=1)
            thresh = cv2.dilate(thresh, kernel, iterations=3)
            
            # Find contours (handles different OpenCV versions)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            detections = []
            for c in cnts:
                if cv2.contourArea(c) < min_area:
                    continue
                
                (x, y, w, h) = cv2.boundingRect(c)
                detections.append({
                    'x': int(x),
                    'y': int(y),
                    'w': int(w),
                    'h': int(h),
                    'area': cv2.contourArea(c)
                })
            
            prev_frame = gray_frame
            frame_count += 1
            # Copy frame to avoid modifying original (displayer will draw on it)
            output_queue.put((frame_num, frame.copy(), detections))
            
    except Exception as e:
        print(f"Error in detector: {e}")
    finally:
        print("Detector: Finished processing")


if __name__ == "__main__":
    test_input = Queue()
    test_output = Queue()
    detector_process(test_input, test_output)

