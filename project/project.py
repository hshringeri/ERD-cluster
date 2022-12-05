# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

import module_1
import module_2
import module_3
import module_4
import module_5
import os

from sklearn.metrics.cluster import rand_score
from colors import bcolors
from sys import platform


def main():
    # User inputs a path to a file
    print(bcolors.OKCYAN+"Module 1: Object-detection Module"+bcolors.ENDC)
    print(bcolors.OKCYAN+"Module 2: OCR Module"+bcolors.ENDC)
    print(bcolors.OKCYAN+"Module 3: Text Processing Module"+bcolors.ENDC)
    print(bcolors.OKCYAN+"Module 4: Base-line Clustering Module"+bcolors.ENDC)
    print(bcolors.OKCYAN+"Module 5: Advanced Clustering Module")
    print(bcolors.OKCYAN +
          "Module 0: Compare Modules 4 and 5 Using Rand-Index Score"+bcolors.ENDC)

    MODULE = input(
        bcolors.OKCYAN+'Choose which module to run (1, 2, 3, 4, 5, 0): '+bcolors.ENDC)
    while MODULE != "1" and MODULE != "2" and MODULE != "3" and MODULE != "4" and MODULE != "5" and MODULE != "0":
        print(bcolors.WARNING +
              'Module input does not equal 1, 2, 3, 4, 5, or 0'+bcolors.ENDC)
        MODULE = input(
            bcolors.OKCYAN+'Enter which module to run (1, 2, 3, 4, 5, 0): '+bcolors.ENDC)

    if MODULE == "1" or MODULE == "2" or MODULE == "3":
        INPUT_IMAGE_PATH = input(
            bcolors.OKCYAN+'Enter a valid filepath to an image: '+bcolors.ENDC)
        # If it is invalid, loop until a vaid path is found
        while not os.path.exists(INPUT_IMAGE_PATH):
            print(bcolors.WARNING+'Image path is not valid \n(hint: cwd of this script is ' +
                  os.getcwd()+bcolors.ENDC)
            INPUT_IMAGE_PATH = input(
                bcolors.OKCYAN + 'Enter a valid filepath to an image: '+bcolors().ENDC)

        # Creates a copy of the input image path to not overwrite original img
        TEMP_FILE_PATH = INPUT_IMAGE_PATH.split(
            '\\') if platform == "win32" else INPUT_IMAGE_PATH.split('/')
        TEMP_FILE = TEMP_FILE_PATH[len(TEMP_FILE_PATH) - 1].split('.')
        TEMP_FILE = TEMP_FILE[0] + '-labled.png'
        TEMP_FILE_PATH[len(TEMP_FILE_PATH) - 1] = TEMP_FILE
        TEMP_FILE_PATH = '\\'.join(
            TEMP_FILE_PATH) if platform == "win32" else '/'.join(TEMP_FILE_PATH)
    else:
        PARAMETERS_FILE_PATH = input(
            bcolors.OKCYAN+'Enter a valid filepath to parameters.txt: '+bcolors.ENDC)
        # If it is invalid, loop until a vaid path is found
        while not os.path.exists(PARAMETERS_FILE_PATH):
            print(bcolors.WARNING+'Parameters path is not valid \n(hint: cwd of this script is ' +
                  os.getcwd()+bcolors.ENDC)
            PARAMETERS_FILE_PATH = input(
                bcolors.OKCYAN + 'Enter a valid filepath to parameters.txt: '+bcolors().ENDC)

    if MODULE == "1":
        print(bcolors.OKGREEN+'Labeled image will be saved at: ' +
              TEMP_FILE_PATH + bcolors.ENDC)
        boxes = module_1.run(INPUT_IMAGE_PATH, TEMP_FILE_PATH, True)
        print(boxes)
    elif MODULE == "2":
        boxes = module_1.run(INPUT_IMAGE_PATH, TEMP_FILE_PATH, False)
        text = module_2.get_all_text_from_image(INPUT_IMAGE_PATH, boxes)
        print(text)
    elif MODULE == "3":
        boxes = module_1.run(INPUT_IMAGE_PATH, TEMP_FILE_PATH, False)
        text = module_2.get_all_text_from_image(INPUT_IMAGE_PATH, boxes)
        processed_text = module_3.process_text(text)
        print(processed_text)
    elif MODULE == "4":
        module_4.runkmeans(PARAMETERS_FILE_PATH, True)
    elif MODULE == "5":
        module_5.runkmeans(PARAMETERS_FILE_PATH, True)
    elif MODULE == "0":
        labels_module_4 = module_4.runkmeans(PARAMETERS_FILE_PATH, False)
        labels_module_5 = module_5.runkmeans(PARAMETERS_FILE_PATH, False)
        print("The rand-index score between the clusterings of modules 4 and 5 is {}".format(
            rand_score(labels_module_4, labels_module_5)))


if __name__ == '__main__':
    main()
