# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

import module_1
import module_2
import module_3
import module_4
from colors import bcolors
import os
from os.path import isfile, join
from sys import platform

def main():
    INPUT_TXT_PATH = input(bcolors.OKCYAN+'Enter a valid filepath to parameters.txt: '+bcolors.ENDC)
    #If it is invalid, loop until a vaid path is found
    while not os.path.exists(INPUT_TXT_PATH):
        print(bcolors.WARNING+'Path is not valid \n(hint: cwd of this script is ' + os.getcwd()+bcolors.ENDC)
        INPUT_TXT_PATH = input(bcolors.OKCYAN +'Enter a valid filepath to parameters.txt: '+bcolors().ENDC)

    with open(INPUT_TXT_PATH, 'r') as f:
        inputs = f.readlines()
    f.close()

    dir_path = inputs[0].replace('\n', '')
    if not os.path.isdir(dir_path):
        print('invalid path')
        exit()
    n_clusters = int(inputs[1])

    img_names = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

    images = []
    for x in img_names:
        boxes = module_1.run(module_1.run(join(dir_path, f), '', False))
        text = module_2.get_all_text_from_image(join(dir_path, f), boxes)
        images.append([x, boxes, text])


if __name__=='__main__':
    main()