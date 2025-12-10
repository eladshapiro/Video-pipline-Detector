"""
Displayer component - draws detections on image, adds timestamp, and displays on screen
"""
import cv2
import datetime
import time
from multiprocessing import Process, Queue

def gaussian_blur_region(image, x, y, w, h, kernel_size=31):
    """
    Apply Gaussian blur to a specific region of the image.
    """
    # Ensure coordinates are within image bounds
    h_img, w_img = image.shape[:2]
    x = max(0, min(x, w_img - 1))
    y = max(0, min(y, h_img - 1))
    w = min(w, w_img - x)
    h = min(h, h_img - y)
    
    if w <= 0 or h <= 0:
        return image
    
    # Ensure kernel_size is odd (required by OpenCV)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Extract the region of interest
    roi = image[y:y+h, x:x+w]
    
    # Apply Gaussian blur
    blurred_roi = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
    
    # Replace the region in the original image
    image[y:y+h, x:x+w] = blurred_roi
    
    return image


def displayer_process(input_queue, fps=None):
    """
    Display process with Gaussian blur for detected motion areas.
    
    Args:
        input_queue: Queue receiving frames and detections
        fps: Frames per second for playback rate
    """
    if fps is None:
        fps = 30
    
    frame_time = 1.0 / fps
    
    try:
        while True:
            data = input_queue.get()
            
            if data is None:
                break
            
            frame_num, frame, detections = data
            
            # Apply Gaussian blur to detected motion areas
            for det in detections:
                x, y, w, h = det['x'], det['y'], det['w'], det['h']
                # Apply Gaussian blur - smooth, natural looking
                frame = gaussian_blur_region(frame, x, y, w, h, kernel_size=31)
                # Draw bounding boxes around detected motion areas (optional - for visualization)
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

