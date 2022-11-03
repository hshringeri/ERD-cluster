import module_1
import module_2
from colors import bcolors
import tensorflow as tf
assert tf.__version__.startswith('2')
from PIL import Image
import os
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

#All of this is to attempt to stop tf from printin to stdout so much
tf.get_logger().setLevel('INFO')
from absl import logging
logging.set_verbosity(logging.INFO)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2Data'

MODEL_PATH = 'Data\Models\model#4-100epcohs.tflite'
DETECTION_THRESHOLD = 0.3

def main():
    #User inputs a path to a file
    INPUT_IMAGE_PATH = input(bcolors.OKCYAN+'Enter a valid filepath to Img: '+bcolors.ENDC)

    #If it is invalid, loop until a vaid path is found
    #TODO add exit condition
    while not os.path.exists(INPUT_IMAGE_PATH):
        print(bcolors.WARNING+'Image Path is not valid \n(hint: cwd of this script is ' + os.getcwd()+bcolors.ENDC)
        INPUT_IMAGE_PATH = input(bcolors.OKCYAN +'Enter a valid filepath to Img: '+bcolors().ENDC)

    #Creates a copy of the input image path to not overwrite original img
    TEMP_FILE_PATH = INPUT_IMAGE_PATH.split('\\')
    TEMP_FILE = TEMP_FILE_PATH[len(TEMP_FILE_PATH) - 1].split('.')
    TEMP_FILE = TEMP_FILE[0] + '-labled.png'
    TEMP_FILE_PATH[len(TEMP_FILE_PATH) - 1] = TEMP_FILE
    TEMP_FILE_PATH = '\\'.join(TEMP_FILE_PATH)
    print(bcolors.OKGREEN+'Labeled image will be saved at: ' + TEMP_FILE_PATH + bcolors.ENDC)

    #creates a copy of the image
    im = Image.open(INPUT_IMAGE_PATH)
    im.save(TEMP_FILE_PATH, 'PNG')

    # Load the TFLite model
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    # Run inference and draw detection result on the local copy of the original file
    detection_result_image, boxes = module_1.run_odt_and_draw_results(
        TEMP_FILE_PATH,
        interpreter,
        threshold=DETECTION_THRESHOLD
    )

    # Show the detection result
    ima = Image.fromarray(detection_result_image)
    ima.save(TEMP_FILE_PATH, 'PNG')

    #display image in a different window
    """ show_img = mpimg.imread(TEMP_FILE_PATH)
    imgplot = plt.imshow(show_img)
    plt.show() """

    print(bcolors.OKGREEN + 'Fin' + bcolors.ENDC)

if __name__=='__main__':
    main()