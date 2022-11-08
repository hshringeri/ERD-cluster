# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma
import cv2
import pytesseract
import os
import numpy as np

def open_image(img_path, coords):
    img = cv2.imread(img_path)
    crop = img[coords[2]:coords[4], coords[1]:coords[3]]
    return crop

def zoom_at(img, zoom, coord=None):
    """
    Simple image zooming without boundary checking.
    Centered at "coord", if given, else the image center.

    img: numpy.ndarray of shape (h,w,:)
    zoom: float
    coord: (float, float)
    """
    # Translate to zoomed coordinates
    h, w = [ zoom * i for i in img.shape ]
    
    if coord is None: cx, cy = w/2, h/2
    else: cx, cy = [ zoom*c for c in coord ]
    
    img = cv2.resize( img, (0, 0), fx=zoom, fy=zoom)
    img = img[ int(round(cy - h/zoom * .3)) : int(round(cy + h/zoom * .3)),
               int(round(cx - w/zoom * .6)) : int(round(cx + w/zoom * .6))]
    
    return img

def preprocess_image(img, object_type, i):
    scale_percent = 200
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    img = cv2.GaussianBlur(img, (3,3), 0)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    if object_type == "attribute":
        blur = cv2.GaussianBlur(img, (3,3), 10)
        ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (200, 1))
        remove_circle = cv2.morphologyEx(blur, cv2.MORPH_OPEN, ellipse_kernel, iterations=1)
        cnts = cv2.findContours(remove_circle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255,255,255), 5)
    elif object_type == "weakrelationship":
        img = zoom_at(img, 1.2)
    elif object_type == "entity" or object_type == "weakentity":
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
        remove_horizontal = cv2.morphologyEx(img, cv2.MORPH_CLOSE, horizontal_kernel, iterations=3)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        mask = np.zeros(img.shape, np.uint8)
        for c in cnts:
            cv2.drawContours(mask, [c], -1, (255,255,255),2)
        img_dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)


    cv2.imwrite("image" + str(i) +".png", img)

    return img

def get_text_from_image(img):
    custom_config = r'--oem 3 --psm 11'
    return pytesseract.image_to_string(img, config=custom_config)

# def clean_up_text(texts):
#     cleaned_up = []
#     for text in texts:
        
#     return cleaned_up

def get_all_text_from_image(img_path, all_coords):
    all_text = []
    for i, coord in enumerate(all_coords):
        img = open_image(img_path, coord)
        img = preprocess_image(img, coord[0], i)
        text = get_text_from_image(img)
        all_text.append([coord[0], text])
    return all_text

# print(get_all_text_from_image("../Collection1/045.png", [['attribute', 1741, 682, 2154, 843], ['relationship', 1663, 281, 2023, 559], ['weakrelationship', 2829, 1245, 3313, 1483], ['weakentity', 1869, 1964, 3024, 2946], ['weakrelationship', 1631, 1323, 2099, 1561], ['weakrelationship', 2, 1282, 485, 1530], ['weakentity', 232, 1862, 1317, 2591], ['entity', 2168, 262, 3187, 694], ['entity', 405, 264, 1433, 1165]]))