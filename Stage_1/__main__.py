# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

import module_1
import module_2
from colors import bcolors
import os
from sys import platform

def main():
    #User inputs a path to a file
    MODULE = input(bcolors.OKCYAN+'Enter which module to run (1 or 2): '+bcolors.ENDC)
    while MODULE != "1" and MODULE != "2":
        print(bcolors.WARNING+'Module input does not equal 1 or 2'+bcolors.ENDC)
        MODULE = input(bcolors.OKCYAN+'Enter which module to run (1 or 2): '+bcolors.ENDC)

    INPUT_IMAGE_PATH = input(bcolors.OKCYAN+'Enter a valid filepath to Img: '+bcolors.ENDC)
    #If it is invalid, loop until a vaid path is found
    while not os.path.exists(INPUT_IMAGE_PATH):
        print(bcolors.WARNING+'Image Path is not valid \n(hint: cwd of this script is ' + os.getcwd()+bcolors.ENDC)
        INPUT_IMAGE_PATH = input(bcolors.OKCYAN +'Enter a valid filepath to Img: '+bcolors().ENDC)

    #Creates a copy of the input image path to not overwrite original img
    TEMP_FILE_PATH = INPUT_IMAGE_PATH.split('\\') if platform == "win32" else INPUT_IMAGE_PATH.split('/')
    TEMP_FILE = TEMP_FILE_PATH[len(TEMP_FILE_PATH) - 1].split('.')
    TEMP_FILE = TEMP_FILE[0] + '-labled.png'
    TEMP_FILE_PATH[len(TEMP_FILE_PATH) - 1] = TEMP_FILE
    TEMP_FILE_PATH = '\\'.join(TEMP_FILE_PATH) if platform == "win32" else '/'.join(TEMP_FILE_PATH)

    if MODULE == "1":
        print(bcolors.OKGREEN+'Labeled image will be saved at: ' + TEMP_FILE_PATH + bcolors.ENDC)
        boxes = module_1.run(INPUT_IMAGE_PATH, TEMP_FILE_PATH, True)
        print(boxes)
    elif MODULE == "2":
        boxes = module_1.run(INPUT_IMAGE_PATH, TEMP_FILE_PATH, False)
        text = module_2.get_all_text_from_image(INPUT_IMAGE_PATH, boxes)
        print(text)


if __name__=='__main__':
    main()