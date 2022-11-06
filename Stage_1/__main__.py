import module_1
#Daimport module_2
from colors import bcolors
import os

def main():
    #User inputs a path to a file
    INPUT_IMAGE_PATH = input(bcolors.OKCYAN+'Enter a valid filepath to Img: '+bcolors.ENDC)

    #If it is invalid, loop until a vaid path is found
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

    boxes = module_1.run(INPUT_IMAGE_PATH, TEMP_FILE_PATH)


if __name__=='__main__':
    main()