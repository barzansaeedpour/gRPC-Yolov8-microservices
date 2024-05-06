from datetime import datetime
import cv2
from bidi.algorithm import get_display
import arabic_reshaper
import time

def get_new_name():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the datetime as desired (e.g., YYYYMMDD-HHMMSS)
    formatted_datetime = current_datetime.strftime("%Y%m%d-%H%M%S")

    # Create a unique filename
    filename = f"my_file_{formatted_datetime}"
    # print(f"Unique filename: {filename}")
    return filename


def persian(text):
    text = get_display(arabic_reshaper.reshape(text))
    return text

def extract_the_plate(img,  top_left, bottom_right):
    plate = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    plate = cv2.resize(plate, (700, 300))
    return plate

def check_detected_classes_validation(detected_classes, numbers, letters, path, boxes):
    not_valid = False
    if len(detected_classes) != 8:
        not_valid = True
    else:    
    #     for i in [0,1,3,4,5,6,7]: 
    #         if detected_classes[i] not in numbers:
    #             not_valid = True
    #     if detected_classes[2] not in letters:
    #         not_valid = True
        
        # sorting
        all_x1s = [x.xyxy[0][0].item() for x in boxes]
        all_x1s, detected_classes = zip(*sorted(zip(all_x1s , detected_classes )))
        
        with open(f"{path}detection.txt", "a") as file:
            # Write content to the file
            text = str(detected_classes)+'\n'
            file.write(f"{text}\n")
            time.sleep(0.1)
    return not_valid
