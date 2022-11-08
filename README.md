# CS-473-Project-1
# Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma
Steps to run Stage 1 of our Project:
1. Be sure to run 'pip install -r requirements.txt' to make sure all dependencies are included
    i. Pytesseract may need additonal instalation, see: https://github.com/UB-Mannheim/tesseract/wiki
2. Run 'python __main__.py' in the Stage_1 folder.
    i. The terminal will ask for a path to an image. The program will save a copy of the image with '-labeled' appended to the name in the same location.
    ii. This image will be labeled with bounding boxes identifying each object within the ERD graph.
    iii.  The terminal will output the list of ERD objects and their contents.

The folder \Stage_1\ contains all of the required python files for Stage 1 of the project

\Stage_1\
    - __main__.py: The main python file. The steps to execute are above.
    - colors.py: A fun class that allows the printing of colored text to the terminal.
    - module_1.py: Python functions that label an image using the trained tf model and returns the bounding boxes
    - module_2.py: Python functions that reads text within the bounding boxes given by module_1.py

Within this project, there is a folder called Data, witch contains all images used to train and test the models, as well as some useful python scripts.

\Data\
    - \AllData-jpgs\: All ~140 images as jpgs
    - \AllData-pngs\: All ~140 images as pngs
    - \Models\: Contains all tf models
        - model#0.tflite: Extremely fast but inaccurate
        - model#4.tflite: Slow but accurate. This is the model used in the project
    - \TestingData\: Contains images\labels used to test the tf model
        - \Annnotations\: XML files corresponding to the \Images\ directory below
        - \Images\: jpg images corresponding to the \Annotations\ above
    - \TrainingData\: Contains images\labels used to train the tf model
        - \Lables\: XML files corresponding to the \Images\ directory below
        - \Images\: jpg images corresponding to the \Annotations\ above
    - \ValidationData\: Contains images\labels used to validate the tf model
        - \Lables\: XML files corresponding to the \Images\ directory below
        - \Images\: jpg images corresponding to the \Annotations\ above
    - png-to-jpg.py: Converts a directory of png images to jpg in a new directory
    - training.py: Trains and automatically saves a tf model into \Models\
    - visualization.py: Script to test the accuracy of a trained tf model