# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

from absl import logging
from sys import platform
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
logging.set_verbosity(logging.ERROR)

MODEL_PATH = 'Data\Models\model#4v2.tflite' if platform == "win32" else 'Data/Models/model#4.tflite'
DETECTION_THRESHOLD = 0.3

# Load the labels into a list
classes = ['entity', 'weakentity', 'relationship',
           'weakrelationship', 'attribute']
label_map = label_map = {1: 'entity', 2: 'weakentity',
                         3: 'relationship', 4: 'weakrelationship', 5: 'attribute'}

# Define a list of colors for visualization
#COLORS = np.random.randint(0, 255, size=(len(classes), 3), dtype=np.uint8)
COLORS = [[73, 229, 11], [182, 31, 193], [
    0, 0, 0], [24, 143, 173], [232, 144, 85]]


def preprocess_image(image_path, input_size):
    """Preprocess the input image to feed to the TFLite model"""
    img = tf.io.read_file(image_path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.uint8)
    original_image = img
    resized_img = tf.image.resize(img, input_size)
    resized_img = resized_img[tf.newaxis, :]
    resized_img = tf.cast(resized_img, dtype=tf.uint8)
    return resized_img, original_image


def detect_objects(interpreter, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""

    signature_fn = interpreter.get_signature_runner()

    # Feed the input image to the model
    output = signature_fn(images=image)

    # Get all outputs from the model
    count = int(np.squeeze(output['output_0']))
    scores = np.squeeze(output['output_1'])
    classes = np.squeeze(output['output_2'])
    boxes = np.squeeze(output['output_3'])

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)
    return results


def run_odt_and_draw_results(image_path, interpreter, threshold=0.5):
    """Run object detection on the input image and draw the detection results"""
    # Load the input shape required by the model
    _, input_height, input_width, _ = interpreter.get_input_details()[
        0]['shape']

    # Load the input image and preprocess it
    preprocessed_image, original_image = preprocess_image(
        image_path,
        (input_height, input_width)
    )

    # Run object detection on the input image
    results = detect_objects(
        interpreter, preprocessed_image, threshold=threshold)

    box_list = []

    # Plot the detection results on the input image
    original_image_np = original_image.numpy().astype(np.uint8)
    for obj in results:
        # Convert the object bounding box from relative coordinates to absolute
        # coordinates based on the original image resolution
        ymin, xmin, ymax, xmax = obj['bounding_box']
        xmin = 0 if int(
            xmin * original_image_np.shape[1]) < 0 else int(xmin * original_image_np.shape[1])
        xmax = original_image.shape[1] if int(
            xmax * original_image_np.shape[1]) >= original_image.shape[1] else int(xmax * original_image_np.shape[1])
        ymin = 0 if int(
            ymin * original_image_np.shape[0]) < 0 else int(ymin * original_image_np.shape[0])
        ymax = original_image.shape[0] if int(
            ymax * original_image_np.shape[0]) >= original_image.shape[0] else int(ymax * original_image_np.shape[0])

        # Find the class index of the current object
        class_id = int(obj['class_id'])

        box_list.append([classes[class_id], xmin, ymin, xmax, ymax])

        # Draw the bounding box and label on the image
        color = [int(c) for c in COLORS[class_id]]
        cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 2)
        # Make adjustments to make the label visible for all objects
        y = ymin - 15 if ymin - 15 > 15 else ymin + 15
        label = "{}: {:.0f}%".format(classes[class_id], obj['score'] * 100)
        cv2.putText(original_image_np, label, (xmin, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Return the final image
    original_uint8 = original_image_np.astype(np.uint8)
    return original_uint8, box_list


def run(INPUT_IMAGE_PATH, TEMP_FILE_PATH, OUTPUT_FILE):
    # Load the TFLite model
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    # Run inference and draw detection result on the local copy of the original file
    detection_result_image, boxes = run_odt_and_draw_results(
        INPUT_IMAGE_PATH,
        interpreter,
        threshold=DETECTION_THRESHOLD
    )

    if OUTPUT_FILE:
        # Show the detection result
        ima = Image.fromarray(detection_result_image)
        ima.save(TEMP_FILE_PATH, 'PNG')
    return boxes
