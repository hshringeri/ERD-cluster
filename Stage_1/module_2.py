# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

import cv2
import pytesseract
import numpy as np
import re


def open_image(img_path, coords):
    img = cv2.imread(img_path)
    crop = img[coords[2]:coords[4], coords[1]:coords[3]]
    return crop


def zoom_at(img, zoom, coord=None):
    h, w = [zoom * i for i in img.shape]

    if coord is None:
        cx, cy = w/2, h/2
    else:
        cx, cy = [zoom*c for c in coord]

    img = cv2.resize(img, (0, 0), fx=zoom, fy=zoom)
    img = img[int(round(cy - h/zoom * .3)): int(round(cy + h/zoom * .3)),
              int(round(cx - w/zoom * .6)): int(round(cx + w/zoom * .6))]

    return img


def preprocess_image(img, object_type, i):
    scale_percent = 200
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    if object_type == "attribute":
        blur = cv2.GaussianBlur(img, (3, 3), 10)
        ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (200, 1))
        remove_circle = cv2.morphologyEx(
            blur, cv2.MORPH_OPEN, ellipse_kernel, iterations=1)
        cnts = cv2.findContours(
            remove_circle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255, 255, 255), 5)
    elif object_type == "weakrelationship":
        img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = cv2.erode(img, None, iterations=1)
        img = zoom_at(img, 1.6)
    elif object_type == "relationship":
        img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = cv2.erode(img, None, iterations=1)
        img = zoom_at(img, 1.6)
    elif object_type == "entity" or object_type == "weakentity":
        gray = cv2.bitwise_not(img)
        bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 15, -2)
        horizontal = np.copy(bw)
        vertical = np.copy(bw)

        cols = horizontal.shape[1]
        horizontal_size = cols / 15
        horizontalStructure = cv2.getStructuringElement(
            cv2.MORPH_RECT, (int(horizontal_size), 1))
        horizontal = cv2.erode(horizontal, horizontalStructure)
        horizontal = cv2.dilate(horizontal, horizontalStructure)

        rows = vertical.shape[0]
        verticalsize = rows / 15
        verticalStructure = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, int(verticalsize)))
        vertical = cv2.erode(vertical, verticalStructure, iterations=3)
        vertical = cv2.dilate(vertical, verticalStructure)

        cnts = cv2.findContours(
            horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255, 255, 255), 5)

        cnts = cv2.findContours(
            vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255, 255, 255), 5)

    # cv2.imwrite("image" + str(i) +".png", img) uncomment to output imave

    return img


def get_text_from_image(img):
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
    return pytesseract.image_to_string(img, config=custom_config)


def clean_up_text(texts):
    cleaned_up = []
    for text in texts:
        text[1] = re.sub('\n', ' ', text[1])
        text[1] = " ".join(text[1].split())
        text[1] = re.sub(r'\b\w{1,2}\b', '', text[1])
        text_list = text[1].split(' ')
        a = []
        while '' in text_list:
            text_list.remove('')
        a.append(text[0])
        for x in text_list:
            a.append(x)
        cleaned_up.append(a)
    return cleaned_up

def get_all_text_from_image(img_path, all_coords):
    all_text = []
    for i, coord in enumerate(all_coords):
        img = open_image(img_path, coord)
        img = preprocess_image(img, coord[0], i)
        text = get_text_from_image(img)
        all_text.append([coord[0], text])
    return clean_up_text(all_text)
