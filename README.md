# CS-473-Project-1
## Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma
## Stage 1
### Prerequisites
1. Install tesseract using [the official installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html).
2. Create a Python environment using `python3 -m venv env`.
3. Run a Python environment using `source env/bin/activate` for MacOS and Linux, or `.\env\Scripts\Activate.ps1` on Windows.
4. Install dependencies using `pip install -r requirements.txt`
5. You need to have an AWS account and have an [access key](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-about)
### Running stage 1
While in the project's root directory, run 'AWS_ACCESS_KEY_ID="" AWS_SECRET_ACCESS_KEY="" python3 ./project/project.py':
    i. It will prompt you to choose a module to run.
    ii. Then, it will prompt for a path to an image relative to the project's root directory.
    iii. If module 1 is chosen, the Python script will save a copy of the image with '-labeled' appended to the name in the same location which contains labels for the objects it detected in the image.
    v.  If module 2 is chosen, the Python script will output the text extracted from that image.

### Project structure
The folder `/project/` contains all of the required Python files for Stage 1 of the project:

`/project/`
- `project.py`: The main python file. The steps to execute are above.
- `colors.py`: A fun class that allows the printing of colored text to the terminal.
- `module_1.py`: Python functions that label an image using the trained tf model and returns the bounding boxes.
- `module_2.py`: Python functions that extracts text within the bounding boxes given by module_1.py.

The folder `/Data/` contains all images used to train and test the models, as well as some useful python scripts:

`\Data\`
- `\AllData-jpgs\`: All ~140 images as jpgs
- `\AllData-pngs\`: All ~140 images as pngs
- `\Models\`: Contains all tf models
    - `model#0.tflite`: Extremely fast but inaccurate
    - `model#4.tflite`: Slow but accurate. This is the model used in the project
- `\TestingData\`: Contains images\labels used to test the tf model
    - `\Annnotations\`: XML files corresponding to the \Images\ directory below
    - `\Images\`: jpg images corresponding to the \Annotations\ above
- `\TrainingData\`: Contains images\labels used to train the tf model
    - `\Lables\`: XML files corresponding to the \Images\ directory below
    - `\Images\`: jpg images corresponding to the \Annotations\ above
- `\ValidationData\`: Contains images\labels used to validate the tf model
    - `\Lables\`: XML files corresponding to the \Images\ directory below
    - `\Images\`: jpg images corresponding to the \Annotations\ above
- `png-to-jpg.py`: Converts a directory of png images to jpg in a new directory
- `training.py`: Trains and automatically saves a tf model into \Models\
    - `visualization.py`: Script to test the accuracy of a trained tf model
