import cv2
import pytesseract
import numpy as np
import copy
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.ext'
def open_image(img_path, coords):
    img = cv2.imread(img_path)
    crop = img[coords[2]:coords[4], coords[1]:coords[3]]
    return crop

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
        ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (200, 1))
        remove_circle = cv2.morphologyEx(img, cv2.MORPH_OPEN, ellipse_kernel, iterations=1)
        cnts = cv2.findContours(remove_circle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255,255,255), 5)
    elif object_type == "weakrelationship":
        thresh_inv = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = np.array([[0, 0, -1],
                           [0, -1, 0],
                           [-1, 0, 0]], dtype=np.uint8)
        opening = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, kernel, iterations=1)
        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 500:
                cv2.drawContours(opening, [c], -1, (0,0,0), -1)

        # cv2.imwrite("opening" + str(i) +".jpg", opening)
        img = cv2.bitwise_xor(img, opening)

    # cv2.imwrite("image" + str(i) +".jpg", img)

    return img

def get_text_from_image(img):
    custom_config = r'--oem 3 --psm 11'
    return pytesseract.image_to_string(img, config=custom_config)

def get_all_text_from_image(img_path, all_coords):
    all_text = []
    for i, coord in enumerate(all_coords):
        img = open_image(img_path, coord)
        img = preprocess_image(img, coord[0], i)
        text = get_text_from_image(img)
        all_text.append([coord[0], text])
    return all_text


print(get_all_text_from_image("Data/TestingData/Images/126.jpg", [['entity', 275, 475, 462, 571], ['attribute', 142, 579, 213, 618], ['weakrelationship', 613, 149, 715, 201], ['weakrelationship', 324, 45, 415, 96], ['attribute', 528, 580, 600, 618], ['weakrelationship', 553, 496, 675, 555], ['attribute', 628, 579, 700, 618], ['weakrelationship', 461, 149, 583, 201], ['weakrelationship', 308, 159, 398, 222], ['weakrelationship', 355, 345, 463, 407], ['weakrelationship', 70, 495, 190, 555], ['attribute', 42, 579, 115, 619], ['weakrelationship', 82, 171, 178, 232], ['weakentity', 457, 2, 722, 136], ['weakentity', 456, 215, 724, 361], ['weakentity', 2, 285, 261, 428], ['entity', 8, 23, 265, 118]]))