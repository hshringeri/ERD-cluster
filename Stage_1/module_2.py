import cv2
import pytesseract
import numpy as np
import copy

def open_image(img_path, coords):
    img = cv2.imread(img_path)
    crop = img[coords[2]:coords[4], coords[1]:coords[3]]
    return crop

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def preprocess_image(img, object_type, i):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    if object_type == "attribute":
        ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (100, 1))
        remove_circle = cv2.morphologyEx(img, cv2.MORPH_OPEN, ellipse_kernel, iterations=1)
        cnts = cv2.findContours(remove_circle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255,255,255), 5)
    elif object_type == "weakrelationship":
        j = 1 #noop

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