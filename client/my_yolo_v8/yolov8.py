from ultralytics import YOLO
import cv2
import os
import shutil
import numpy as np
import math
import time
from PIL import ImageFont, ImageDraw, Image
from my_yolo_v8.rabbitmq.publisher import publish

from my_yolo_v8.utils.utils import extract_the_plate, check_detected_classes_validation, get_new_name, persian



model_plate_detection = YOLO(f"./my_yolo_v8/models/plate-detector.pt")
model_character_detection = YOLO(f"./my_yolo_v8/models/character-detector.pt")

plate_detection_output_path = "/code/my_yolo_v8/outputs/"
try:
    shutil.rmtree(plate_detection_output_path)
except:
    pass
os.makedirs(plate_detection_output_path, exist_ok=True)

plate_detection_path = './my_yolo_v8/outputs2/plate_detection_path/'
character_detection_path = './my_yolo_v8/outputs2/character_detection_path/'

classNames = ['plate']
# classNames2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'be', 'dal', 'ein', 'ghaf', 'h', 'jim', 'lam', 'mim', 'noon', 'sad', 'sin', 'ta', 'te', 'waw', 'ye']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
# letters = ['alef', 'be', 'che', 'dal', 'ein', 'ghaf', 'h', 'jim', 'lam', 'mim', 'noon', 'sad', 'sin', 'ta', 'te', 'waw', 'ye']
# letters = ['alef', 'be', 'che', 'ein', 'dal',  'ghaf', 'h', 'jim', 'lam', 'mim', 'noon', 'sad', 'sin', 'ta', 'te', 'waw', 'ye']
# letters = ['alef', 'be', 'che', 'dal', 'ein', 'jim', 'h', 'ghaf', 'lam', 'sad', 'noon', 'mim', 'sin', 'ta', 'te', 'waw', 'ye']
letters = ['be', 'dal', 'ein', 'ghaf', 'h', 'jim', 'lam', 'mim', 'noon', 'sad', 'sin', 'ta', 'te', 'waw', 'ye']

classNames2 = numbers + letters
# classNames2 = list(model_character_detection.names.values())


def plate_detection(frame):
    img = frame
    results = model_plate_detection.predict(source=img, conf = 0.1, save=False, show = False, project=plate_detection_output_path, name="", save_txt = False) 
    for r in results:
            boxes = r.boxes

    for box in boxes:
        # bounding box
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

        try:
            extracted_plate_image = extract_the_plate(img=img, top_left=(x1, y1), bottom_right=(x2, y2))
        except:
            continue
        new_name = get_new_name()
       
        results2 = model_character_detection.predict(source=extracted_plate_image, conf = 0.1, save=False, show = False, project=plate_detection_output_path, name="", save_txt = False) 
        
    
        for r in results2:
            boxes = r.boxes
            detected_classes = [int(box.cls) for box in boxes]   
            
            detected_classes = [classNames2[i] for i in detected_classes]
            continue_flag, detected_classes = check_detected_classes_validation(detected_classes, numbers, letters, plate_detection_output_path, boxes)
        if continue_flag:
            continue    
        img = Image.fromarray(extracted_plate_image)
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->", confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames2[cls])

            # object details
            org = [x1, y1-20]
            
            try:
                img = Image.fromarray(img)
            except:
                pass
            draw = ImageDraw.Draw(img)
            draw.rectangle([(x1, y1), (x2, y2)], outline ='red',)

            text = classNames2[cls]
            color = (0, 0, 255)  # Red color
            draw.rectangle([(org[0], org[1]), (org[0]+(len(text)*15), org[1]+25)], fill =(255,100,100))
            draw.text(org, persian(text), fill=(255,255,255))
            img = np.array(img)

        img = np.array(img)
        cv2.imwrite(plate_detection_output_path + new_name +'.png',img)
        time.sleep(0.1)
        return detected_classes
        # cv2.imshow("Real-time Webcam", img)
        # time.sleep(0.1)
    return ''