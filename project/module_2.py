# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

import cv2
import boto3
import uuid
import os

def get_text_with_textract(img_path, object_coords):
    img = cv2.imread(img_path)
    object_texts = [[coord[0], coord[5], ""] for coord in object_coords]

    with open(img_path, 'rb') as document:
        imageBytes = bytearray(document.read())
    textract = boto3.client('textract',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    response = textract.detect_document_text(Document={'Bytes': imageBytes})

    for item in response["Blocks"]:
        if item["BlockType"] == "LINE" or item["BlockType"] == "WORD":
            text_coord = [int(item["Geometry"]["BoundingBox"]["Left"] * img.shape[1]),
                          int(item["Geometry"]["BoundingBox"]["Top"] * img.shape[0])]
            object_id = match_text_with_object(text_coord, object_coords)
            if not object_id == None:
                for i, object in enumerate(object_texts):
                    if str(object[1]) == str(object_id):
                        object_texts[i][2] += item["Text"] + " "
                        break

    return [[object[0], object[2][:len(object[2])//2].strip()] for object in object_texts]


def match_text_with_object(text_coord, object_coords):
    for coord in object_coords:
        if (text_coord[0] >= coord[1] and text_coord[0] <= coord[3]) and (text_coord[1] >= coord[2] and text_coord[1] <= coord[4]):
            return coord[5]
    return None


def get_all_text_from_image(img_path, object_coords):
    for i in range(len(object_coords)):
        object_coords[i].append(uuid.uuid4())

    return get_text_with_textract(img_path, object_coords)
